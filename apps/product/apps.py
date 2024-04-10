from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.product"
    verbose_name = "بخش محصولات"

    def ready(self):
        import apps.product.signals
