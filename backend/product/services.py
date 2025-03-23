from .models import Product
from mongoengine.errors import DoesNotExist

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
        product = ProductService.get_product(product_id).modify(**data)
        return product
    
    @staticmethod
    def delete(product_id):
        product = ProductService.get_product(product_id).delete()
        return product