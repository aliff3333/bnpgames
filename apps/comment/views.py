from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .forms import ReviewForm
from .models import Review
from ..product.models import BoardGame


class ReviewView(FormMixin, ListView):
    model = Review
    form_class = ReviewForm
    template_name = 'product/partials/Reviews.html'
    context_object_name = 'reviews'
    success_url = "#"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(product=self.kwargs.get('product'), approved=True).select_related('user')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['product_id'] = self.kwargs.get('product')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        body = form.cleaned_data.get('body')
        rating = form.cleaned_data.get('rating')
        product_id = self.kwargs.get('product')

        existing_review = Review.objects.filter(product_id=product_id, user=self.request.user).first()
        if existing_review:
            # Check if the existing review is approved
            if existing_review.approved:
                messages.warning(self.request, "شما از قبل یک بررسی تایید شده دارید.")
                return redirect(reverse('comment:review_list', kwargs={'product': product_id}))
            else:
                messages.warning(self.request, "شما از قبل یک بررسی تایید نشده دارید.")
                return redirect(reverse('comment:review_list', kwargs={'product': product_id}))

        review = Review(body=body, rating=rating, user=self.request.user, product_id=product_id)
        review.save()
        messages.success(self.request, "بررسی شما بعد از تایید مدیر سایت نمایش داده خواهد شد.")
        return redirect(reverse('comment:review_list', kwargs={'product': product_id}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
