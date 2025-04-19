from .models import Product
from .models import ProductCategory
from datetime import datetime


class ProductRepository:
    @staticmethod
    def get_product(product_id):
        return Product.objects.get(id=product_id)

    @staticmethod
    def get():
        return Product.objects.all()

    @staticmethod
    def get_by_category(category_id):
        return Product.objects.filter(category=category_id)

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product_id, data):
        data["updated_at"] = datetime.utcnow()
        product = ProductRepository.get_product(product_id).modify(**data)
        return product

    @staticmethod
    def delete(product_id):
        product = ProductRepository.get_product(product_id).delete()
        return product


class ProductCategoryRepository:
    @staticmethod
    def get_category(category_id):
        return ProductCategory.objects.get(id=category_id)

    @staticmethod
    def get_by_title(title):
        return ProductCategory.objects.get(title=title)

    @staticmethod
    def get():
        return ProductCategory.objects.all()

    @staticmethod
    def create(data):
        category = ProductCategory(**data)
        category.save()
        return category

    @staticmethod
    def update(category_id, data):
        category = ProductCategoryRepository.get_category(category_id).modify(**data)
        return category

    @staticmethod
    def delete(category_id):
        category = ProductCategoryRepository.get_category(category_id).delete()
        return category
