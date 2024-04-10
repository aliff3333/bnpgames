from django import forms
from utils.persian_slugify import persian_slugify
from .models import ProductImage, Category, BoardGame, Mechanism, Designer, Publisher

PRODUCT_MODEL = BoardGame


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'featured']


class SlugifyModelForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk or 'title' in self.changed_data:
            title = self.cleaned_data.get('title')
            if title:
                # Generate slug
                slug = persian_slugify(title)

                # Check if the slug is unique, if not, append a number to make it unique
                num = 1
                while self._meta.model.objects.exclude(pk=instance.pk).filter(slug=slug).exists():
                    slug = f"{slug}-{num}"
                    num += 1

                instance.slug = slug

        if commit:
            instance.save()
        return instance


class ProductAdminForm(SlugifyModelForm):
    class Meta:
        model = PRODUCT_MODEL
        exclude = ['slug']


class PublisherAdminForm(SlugifyModelForm):
    class Meta:
        model = Publisher
        exclude = ['slug']


class CategoryAdminForm(SlugifyModelForm):
    class Meta:
        model = Category
        exclude = ['slug']


class DesignerAdminForm(SlugifyModelForm):
    class Meta:
        model = Designer
        exclude = ['slug']


class MechanismAdminForm(SlugifyModelForm):
    class Meta:
        model = Mechanism
        exclude = ['slug']


class BoardGameFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False,
                                                widget=forms.CheckboxSelectMultiple())
    mechanisms = forms.ModelMultipleChoiceField(queryset=Mechanism.objects.all(), required=False,
                                                widget=forms.CheckboxSelectMultiple())
    min_price = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    max_price = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    player_count = forms.IntegerField(max_value=20, min_value=1, required=False, label='تعداد بازیکنان')
    time = forms.IntegerField(max_value=500, min_value=1, required=False, label='حداکثر زمان بازی')
    age = forms.IntegerField(max_value=18, min_value=3, required=False, label='حداقل سن بازیکنان')
    available = forms.BooleanField(required=False, label='فقط کالاهای موجود')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in ['age', 'time', 'player_count']:
            self.fields[key].widget.attrs['style'] = "width: 25%; box-sizing: border-box; margin-bottom: 10px;"
        self.fields['available'].widget.attrs['style'] = "float: left;"
