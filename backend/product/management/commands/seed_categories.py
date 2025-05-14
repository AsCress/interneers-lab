import logging
from django.core.management.base import BaseCommand
from product.services.services import ProductCategoryService
from product.services.exceptions import CategoryValidationException

DEFAULT_CATEGORIES = [
    {"title": "Food", "description": ""},
    {"title": "Kitchen Essentials", "description": ""},
    {"title": "Electronics", "description": ""},
    {"title": "Clothing", "description": ""},
    {"title": "Uncategorized", "description": ""},
]

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seeds the database with default categories"

    def handle(self, *args, **kwargs):
        for category_data in DEFAULT_CATEGORIES:
            try:
                category = ProductCategoryService.create(category_data)
            except CategoryValidationException as e:
                logger.warning(f"Error creating category: {category_data['title']}")
            logger.info(f"Created category: {category_data['title']}")

        logger.info("Category seeding complete.")
