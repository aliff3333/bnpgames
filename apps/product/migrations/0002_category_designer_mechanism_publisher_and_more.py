# Generated by Django 5.0.2 on 2024-03-17 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="نام")),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "image",
                    models.ImageField(upload_to="categories", verbose_name="تصویر"),
                ),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="Designer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="نام")),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "image",
                    models.ImageField(upload_to="categories", verbose_name="تصویر"),
                ),
            ],
            options={
                "verbose_name": "طراح بازی",
                "verbose_name_plural": "طراحین بازی",
            },
        ),
        migrations.CreateModel(
            name="Mechanism",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="نام")),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "image",
                    models.ImageField(upload_to="categories", verbose_name="تصویر"),
                ),
            ],
            options={
                "verbose_name": "مکانیزم",
                "verbose_name_plural": "مکانیزم ها",
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="نام")),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "image",
                    models.ImageField(upload_to="categories", verbose_name="تصویر"),
                ),
            ],
            options={
                "verbose_name": "ناشر",
                "verbose_name_plural": "ناشرین",
            },
        ),
        migrations.AddField(
            model_name="boardgame",
            name="stock",
            field=models.PositiveIntegerField(default=0, verbose_name="موجودی"),
        ),
        migrations.AlterField(
            model_name="boardgame",
            name="discount",
            field=models.PositiveSmallIntegerField(
                default=0, verbose_name="درصد تخفیف"
            ),
        ),
        migrations.AddField(
            model_name="boardgame",
            name="categories",
            field=models.ManyToManyField(to="product.category"),
        ),
        migrations.AddField(
            model_name="boardgame",
            name="designers",
            field=models.ManyToManyField(to="product.designer"),
        ),
        migrations.AddField(
            model_name="boardgame",
            name="mechanisms",
            field=models.ManyToManyField(to="product.mechanism"),
        ),
        migrations.AddField(
            model_name="boardgame",
            name="publisher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="product.publisher",
            ),
        ),
    ]
