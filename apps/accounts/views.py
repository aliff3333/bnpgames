from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from allauth.account.views import LogoutView

from .forms import AddressCreationForm
from .models import Address
from ..order.models import Order


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        last_order = Order.objects.filter(
            user=request.user,
            is_paid=True
        ).only('total_price', 'payment_date',
               'status', 'post_code').prefetch_related('items').order_by('-payment_date').first()
        context = {
            'last_order': last_order,
        }
        return render(request, 'accounts/user_profile.html', context)


class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'accounts/factors.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user, is_paid=True).order_by('-payment_date')
        return queryset


class AddressListCreationView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddressCreationForm(user=request.user)
        addresses = Address.objects.filter(user=request.user)

        return render(request, 'accounts/addresses.html', {'form': form, 'addresses': addresses})

    def post(self, request):
        form = AddressCreationForm(data=request.POST, user=request.user)
        addresses = Address.objects.filter(user=request.user)
        user_address_count = Address.objects.filter(user=request.user).count()
        try:
            if user_address_count >= 5:
                raise ValidationError("نمی توانید بیش از 5 آدرس ثبت کنید")
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
        except:
            form.add_error(None, "نمی توانید بیش از 5 آدرس ثبت کنید")

        next_page = request.POST.get('next')
        if next_page:
            return redirect(next_page)

        return render(request, 'accounts/addresses.html', {'form': form, 'addresses': addresses})


class AddressDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        address.delete()

        return redirect('accounts:add_list_address')


class AddressSetActive(LoginRequiredMixin, View):
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        address.is_active = True
        address.save()

        return redirect('accounts:add_list_address')


class CustomLogoutView(LogoutView):
    def get(self, *args, **kwargs):
        raise Http404
