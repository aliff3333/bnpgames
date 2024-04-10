from django.contrib import admin
from django.forms import inlineformset_factory

from . import models, forms
from apps.comment.models import Review


ProductImageFormSet = inlineformset_factory(models.BoardGame, models.ProductImage, form=forms.ProductImageForm, extra=1)


class ReviewInline(admin.TabularInline):
    model = Review


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    formset = ProductImageFormSet


@admin.register(models.BoardGame)
class BoardgameAdmin(admin.ModelAdmin):
    form = forms.ProductAdminForm
    list_display = [
        'title',
        'price',
        'discount',
        'discounted_price_display',
        'stock',
        'publisher',
        'featured',
        'visits',
        'is_active',
    ]
    list_filter = ['is_active']
    inlines = [ProductImageInline, ReviewInline]

    def get_queryset(self, request):
        return models.BoardGame.objects.all()

    def discounted_price_display(self, obj):
        return obj.discounted_price()

    discounted_price_display.short_description = 'قیمت با تخفیف'


@admin.register(models.Publisher)
class Model1Admin(admin.ModelAdmin):
    form = forms.PublisherAdminForm


@admin.register(models.Category)
class Model1Admin(admin.ModelAdmin):
    form = forms.CategoryAdminForm


@admin.register(models.Designer)
class Model1Admin(admin.ModelAdmin):
    form = forms.DesignerAdminForm


@admin.register(models.Mechanism)
class Model1Admin(admin.ModelAdmin):
    form = forms.MechanismAdminForm

