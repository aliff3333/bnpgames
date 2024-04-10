from django.core.exceptions import ValidationError
from django.db import models

from tinymce.models import HTMLField


class HomeSlide(models.Model):
    image = models.ImageField(upload_to='home/slides', verbose_name='تصویر اسلاید')
    url = models.URLField(null=True, blank=True, verbose_name='آدرس')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدها'

    def __str__(self):
        return self.image.name


class HomeBanner(models.Model):
    image = models.ImageField(upload_to='home/banners', verbose_name='تصویر بنر')
    url = models.URLField(verbose_name='آدرس')

    class Meta:
        verbose_name = 'بنر کنار اسلایدر'
        verbose_name_plural = 'بنرهای کنار اسلایدر'

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        if HomeBanner.objects.count() >= 3:
            raise ValidationError("نمی توانید بیش از 3 بنر بسازید")

        super().save(*args, **kwargs)


class AboutUs(models.Model):
    content = HTMLField()
    is_active = models.BooleanField(default=False, verbose_name='فعال')

    class Meta:
        verbose_name = 'محتویات صفحه درباره ما'
        verbose_name_plural = 'محتویات صفحه درباره ما'

    def __str__(self):
        return 'محتویات صفحه درباره ما'

    def save(self, *args, **kwargs):
        if self.is_active:
            AboutUs.objects.exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)
