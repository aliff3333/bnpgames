# Generated by Django 5.0.2 on 2024-02-25 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_rename_full_name_address_receiver"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="آدرس فعال"),
        ),
    ]
