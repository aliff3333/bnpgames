from django.contrib.auth import get_user_model
from django.db import models

from apps.product.models import BoardGame

PRODUCT_MODEL = BoardGame


class BaseComment(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    body = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    approved = models.BooleanField(default=False, verbose_name='تایید شده')

    class Meta:
        abstract = True


class Review(BaseComment):
    name = None
    email = None
    rating = models.IntegerField(default=3, verbose_name='امتیاز')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(PRODUCT_MODEL, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        verbose_name = 'بررسی'
        verbose_name_plural = 'بررسی ها'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.product.title} - {self.user.full_name} - {self.rating}'
