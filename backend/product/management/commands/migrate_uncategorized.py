from django.core.management.base import BaseCommand
from mongoengine.errors import ValidationError
from product.services import ProductCategoryService
from product.services import ProductService


class Command(BaseCommand):
    help = "Migrate products with no category to 'Uncategorized'"

    def handle(self, *args, **kwargs):
        uncategorized_category = ProductCategoryService.get_category_by_title(
            title="Uncategorized"
        )

        uncategorized_products = ProductService.get_by_category(category_id=None)

        for product in uncategorized_products:
            product.category = uncategorized_category
            try:
                product.save()
            except ValidationError:
                self.stderr.write(
                    self.style.ERROR(f"Failed to update product {product.id}")
                )

        self.stdout.write(self.style.SUCCESS(f"Migration complete."))
