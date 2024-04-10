from django.db.models import Prefetch, Case, Value, When, IntegerField
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import HomeSlide, HomeBanner, AboutUs
from apps.product.models import BoardGame, Category, Mechanism, ProductImage, Designer, Publisher


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        base_queryset = BoardGame.active_objects.filter(stock__gt=0).prefetch_related(
            Prefetch(
                'images', queryset=ProductImage.objects.filter(featured=True)),
            'categories').only('title',
                               'price',
                               'discount',
                               'rating',
                               'slug',
                               'images').annotate(
            in_stock=Case(
                When(stock__gt=0, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        context = {
            'sliders': HomeSlide.objects.all(),
            'side_banners': HomeBanner.objects.all(),
            'featured_products': base_queryset.filter(featured=True).order_by('-created_at')[:12],
            'on_sale_products': base_queryset.filter(discount__gt=0).order_by('-created_at')[:12],
            'most_visited': base_queryset.order_by('-visits')[:12],
            'most_sold': base_queryset.order_by('-sales')[:12],
        }
        self.get_featured_image(context['featured_products'])
        self.get_featured_image(context['on_sale_products'])
        self.get_featured_image(context['most_visited'])
        self.get_featured_image(context['most_sold'])

        return context

    @staticmethod
    def get_featured_image(products):
        for product in products:
            for image in product.images.all():
                if image.featured:
                    product.featured_image = image


class ProductGroupsView(TemplateView):
    template_name = 'partials/categories_dropdown.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = Category.objects.all()
        mechanisms = Mechanism.objects.all()
        designers = Designer.objects.all()
        publishers = Publisher.objects.all()
        context['categories'] = categories
        context['mechanisms'] = mechanisms
        context['designers'] = designers
        context['publishers'] = publishers
        return context


class AboutUsView(TemplateView):
    template_name = 'home/about_us.html'

    def get_context_data(self, **kwargs):
        context = {
            'about_us': AboutUs.objects.filter(is_active=True).first(),
        }
        return context
