# Generated by Django 5.0.2 on 2024-02-25 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_address_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="full_name",
            new_name="receiver",
        ),
    ]
