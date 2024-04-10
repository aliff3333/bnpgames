from django.db import models
from django.contrib.auth import get_user_model
from django.views import View

from apps.product.models import BoardGame
from apps.accounts.models import Address

# user model
USER = get_user_model()
PRODUCT = BoardGame


class Order(models.Model):
    STATUS_CHOICES = (
        ('در انتظار تایید', 'در انتظار تایید'),
        ('در حال آماده سازی', 'در حال آماده سازی'),
        ('تحویل پست داده شده', 'تحویل پست داده شده'),
        ('دریافت شده', 'دریافت شده'),
    )

    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='orders')
    receiver_info = models.TextField(null=True, blank=True, verbose_name='اطلاعات گیرنده')
    total_original_price = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='مجموع کل اصلی')
    discounted_price = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='مجموع تخفیف')
    total_price = models.PositiveIntegerField(default=0, verbose_name='مجموع پس از نخفیف')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ و ساعت پرداخت')
    ref_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره پیگیری')
    post_code = models.CharField(max_length=25, null=True, blank=True, verbose_name='کد پیگیری پستی')
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS_CHOICES, verbose_name='وضعیت سفارش')
    post_price = models.PositiveIntegerField(default=0, verbose_name='هزینۀ پست')

    readonly_fields = ('total_original_price', )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'{self.id} - {self.user.full_name}'

    def __len__(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='کاربر')
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد')
    original_price = models.PositiveIntegerField(verbose_name='قیمت اصلی')
    discounted_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت با تخفیف')

    class Meta:
        verbose_name = 'محصول خریداری شده'
        verbose_name_plural = 'محصولات خریداری شده'

    def __str__(self):
        return f'{self.product} x{self.quantity}'
