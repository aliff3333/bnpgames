# Generated by Django 5.0.2 on 2024-04-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0008_remove_orderitem_price_order_total_original_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="تاریخ و ساعت پرداخت"
            ),
        ),
    ]