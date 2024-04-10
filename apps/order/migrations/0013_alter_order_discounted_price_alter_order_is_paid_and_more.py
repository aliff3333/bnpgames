# Generated by Django 5.0.2 on 2024-04-10 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0012_remove_order_discount_code_order_post_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="discounted_price",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="مجموع تخفیف"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="is_paid",
            field=models.BooleanField(default=False, verbose_name="پرداخت شده"),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="تاریخ و ساعت پرداخت"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="post_code",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="کد پیگیری پستی"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="ref_id",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="شماره پیگیری"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="وضعیت سفارش"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_original_price",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="مجموع کل اصلی"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.PositiveIntegerField(
                default=0, verbose_name="مجموع پس از نخفیف"
            ),
        ),
    ]