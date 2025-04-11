from django.core.management.base import BaseCommand
from product.serializers import ProductCategorySerializer
from product.services import ProductCategoryService

DEFAULT_CATEGORIES = [
    {"title": "Food", "description": ""},
    {"title": "Kitchen Essentials", "description": ""},
    {"title": "Electronics", "description": ""},
    {"title": "Clothing", "description": ""},
    {
        "title": "Uncategorized",
        "description": "",
    },
]


class Command(BaseCommand):
    help = "Seeds the database with default categories"

    def handle(self, *args, **kwargs):
        for category_data in DEFAULT_CATEGORIES:
            serializer = ProductCategorySerializer(data=category_data)
            if serializer.is_valid():
                category = serializer.validated_data
                ProductCategoryService.create(category)
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_data["title"]}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Error creating category: {category_data["title"]}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Category seeding complete."))
