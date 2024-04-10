from urllib.parse import urlencode

from django.db.models import Prefetch, Case, IntegerField, Value, When
from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import DetailView, TemplateView, ListView

from .models import BoardGame, Category, Mechanism, ProductImage, Publisher, Designer
from .forms import BoardGameFilterForm

PRODUCT_MODEL = BoardGame


class BoardGameDetailView(DetailView):
    model = BoardGame
    template_name = 'product/product_detail.html'

    def get_object(self):
        obj = super().get_object()

        visited_products = self.request.session.get('visited_products', [])

        if obj.pk not in visited_products:
            obj.visits += 1
            obj.save()
            visited_products.append(obj.pk)
            self.request.session['visited_products'] = visited_products

        return obj


class ProductListView(ListView):
    model = PRODUCT_MODEL
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    form_class = BoardGameFilterForm

    def dispatch(self, request, *args, **kwargs):
        self.ordering = request.GET.get('ordering')
        self.search_query = None
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        template_name = super(ProductListView, self).get_template_names()
        if self.ordering:
            template_name = 'product/partials/products.html'
        return template_name

    def get_queryset(self):
        queryset = PRODUCT_MODEL.active_objects.all()
        form = self.get_form()
        if form.is_valid():
            cleaned_data = form.cleaned_data
            filter_data = {}
            if cleaned_data.get('available'):
                filter_data['stock__gt'] = 0
            if cleaned_data.get('min_price'):
                filter_data['price__gte'] = cleaned_data['min_price']
            if cleaned_data.get('max_price'):
                filter_data['price__lte'] = cleaned_data['max_price']
            if cleaned_data.get('categories'):
                filter_data['categories__in'] = cleaned_data['categories']
            if cleaned_data.get('mechanisms'):
                filter_data['mechanisms__in'] = cleaned_data['mechanisms']
            if cleaned_data.get('player_count'):
                filter_data['player_count_max__gte'] = cleaned_data['player_count']
                filter_data['player_count_min__lte'] = cleaned_data['player_count']
            if cleaned_data.get('time'):
                filter_data['time_max__lte'] = cleaned_data['time']
            if cleaned_data.get('age'):
                filter_data['age__gte'] = cleaned_data['age']
            if filter_data:
                queryset = queryset.filter(**filter_data)

        queryset = queryset.prefetch_related(
            Prefetch('images',
                     queryset=ProductImage.objects.filter(featured=True)),
            'categories', 'mechanisms', 'publisher', 'designers').only('title', 'price', 'discount', 'rating', 'slug', 'reviews').annotate(
            in_stock=Case(
                When(stock__gt=0, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        return self.product_list_ordering(queryset, self.ordering)

    @staticmethod
    def product_list_ordering(queryset, ordering):
        match ordering:
            case 'most-expensive':
                queryset = queryset.order_by('-in_stock', '-price')
            case 'cheapest':
                queryset = queryset.order_by('-in_stock', 'price')
            case 'newest':
                queryset = queryset.order_by('-in_stock', '-created_at')
            case _:
                queryset = queryset.order_by('-in_stock', '-created_at')
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        form = self.get_form()
        query_string = self.construct_query_string(form)
        context_updates = {
            'page_hero_title': 'تمام محصولات',
            'page_hero_description': 'تمام محصولات روبیک مارکت',
            'page_hero_current': 'محصولات',
            'ordering': self.request.GET.get('ordering'),
            'product_count': self.get_queryset().count(),
            'form': form,
            'query_string': "&" + query_string if query_string else ''
        }
        context.update(context_updates)
        self.get_featured_image(context['products'])
        return context

    @staticmethod
    def get_featured_image(products):
        for product in products:
            for image in product.images.all():
                if image.featured:
                    product.featured_image = image

    def get_form(self):
        return self.form_class(self.request.GET)

    def construct_query_string(self, form):
        query_params = self.request.GET.copy()
        if query_params.get('ordering'):
            del query_params['ordering']
        if query_params.get('page'):
            del query_params['page']
        return urlencode(query_params)


class CategoryProductListView(ProductListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=slug)
        queryset = super().get_queryset().filter(categories=self.category.id)
        ordering = self.request.GET.get('ordering')

        return self.product_list_ordering(queryset, ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_hero_title'] = self.category.title
        context['page_hero_description'] = self.category.description
        context['page_hero_mid'] = 'دسته بندی ها'
        context['page_hero_current'] = self.category.title
        return context


class MechanismProductListView(ProductListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        self.mechanism = get_object_or_404(Mechanism, slug=slug)
        queryset = super().get_queryset().filter(mechanisms=self.mechanism.id)
        ordering = self.request.GET.get('ordering')

        return self.product_list_ordering(queryset, ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_hero_title'] = self.mechanism.title
        context['page_hero_mid'] = 'مکانیزم ها'
        context['page_hero_description'] = self.mechanism.description
        context['page_hero_current'] = self.mechanism.title
        return context


class DesignerProductListView(ProductListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        self.designer = get_object_or_404(Designer, slug=slug)
        queryset = super().get_queryset().filter(designers=self.designer.id)
        ordering = self.request.GET.get('ordering')

        return self.product_list_ordering(queryset, ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_hero_title'] = self.designer.title
        context['page_hero_mid'] = 'طراحان'
        context['page_hero_description'] = self.designer.description
        context['page_hero_current'] = self.designer.title
        return context


class PublisherProductListView(ProductListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        self.publisher = get_object_or_404(Publisher, slug=slug)
        queryset = super().get_queryset().filter(publisher=self.publisher.id)
        ordering = self.request.GET.get('ordering')

        return self.product_list_ordering(queryset, ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_hero_title'] = self.publisher.title
        context['page_hero_mid'] = 'ناشران'
        context['page_hero_description'] = self.publisher.description
        context['page_hero_current'] = self.publisher.title
        return context


class SearchProductListView(ProductListView):
    def get_queryset(self):
        self.search_query = self.request.GET.get('q')
        queryset = super().get_queryset().filter(title__icontains=self.search_query)
        ordering = self.request.GET.get('ordering')

        return self.product_list_ordering(queryset, ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_hero_title'] = f'نتایج جستجو برای "{self.search_query}"'
        context['page_hero_description'] = ''
        context['page_hero_mid'] = 'تمام محصولات'
        context['page_hero_current'] = "جستجو"
        print(context['query_string'])
        return context

