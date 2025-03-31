from .models import Product
from .models import ProductCategory
from mongoengine.errors import DoesNotExist
from datetime import datetime


class ProductService:
    @staticmethod
    def get_product(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise DoesNotExist("Product does not exist")

    @staticmethod
    def get():
        return Product.objects.all()

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product_id, data):
        data["updated_at"] = datetime.utcnow()
        product = ProductService.get_product(product_id).modify(**data)
        return product

    @staticmethod
    def delete(product_id):
        product = ProductService.get_product(product_id).delete()
        return product


class ProductCategoryService:
    @staticmethod
    def get_category(category_id):
        try:
            return ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            raise DoesNotExist("Category does not exist")

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
        category = ProductCategoryService.get_category(category_id).modify(**data)
        return category

    @staticmethod
    def delete(category_id):
        category = ProductCategoryService.get_category(category_id).delete()
        return category
