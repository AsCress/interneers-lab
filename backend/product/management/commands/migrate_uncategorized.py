import logging
from django.core.management.base import BaseCommand
from mongoengine.errors import ValidationError
from product.services.services import ProductService
from product.repository.repository import ProductCategoryRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate products with no category to 'Uncategorized'"

    def handle(self, *args, **kwargs):
        uncategorized_category = ProductCategoryRepository.get_by_title(
            title="Uncategorized"
        )

        uncategorized_products = ProductService.get_by_category(category_id=None)

        for product in uncategorized_products:
            product.category = uncategorized_category
            try:
                product.save()
                logger.info(f"Updated product {product.id} to 'Uncategorized'")
            except ValidationError:
                logger.error(f"Failed to update product {product.id}")

        logger.info("Migration complete.")
