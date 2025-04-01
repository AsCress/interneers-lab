from django.apps import AppConfig
from django.core.management import call_command


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"

    def ready(self):
        call_command("seed_categories")
