# Generated by Django 5.0.2 on 2024-04-05 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0003_productcomment_approved_review_approved_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProductComment",
        ),
    ]