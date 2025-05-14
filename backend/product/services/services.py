from ..models import Product, ProductCategory
from ..serializers import ProductSerializer
from ..serializers import ProductCategorySerializer
from ..repository.repository import ProductRepository
from ..repository.repository import ProductCategoryRepository
from ..repository.exceptions import ProductDoesNotExist
from ..repository.exceptions import CategoryDoesNotExist
from ..repository.exceptions import ProductValidationError
from ..repository.exceptions import CategoryValidationError
from .exceptions import ProductNotFoundException
from .exceptions import CategoryNotFoundException
from .exceptions import ProductValidationException
from .exceptions import CategoryValidationException


class ProductService:

    @staticmethod
    def get():
        products = ProductRepository.get()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @staticmethod
    def get_by_id(product_id):
        try:
            product = ProductRepository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        serializer = ProductSerializer(product)
        return serializer.data

    @staticmethod
    def get_by_category(category_id):
        products = ProductRepository.get_by_category(category_id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    @staticmethod
    def create(data):
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.validated_data
            ProductRepository.create(product)
        else:
            raise ProductValidationException(errors=serializer.errors)
        return serializer.data

    @staticmethod
    def update(product_id, data):
        try:
            product = ProductRepository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        serializer = ProductSerializer(product, data, partial=True)
        if serializer.is_valid():
            product = serializer.validated_data
            ProductRepository.update(product_id, product)
        else:
            raise ProductValidationException(product_id, serializer.errors)
        return serializer.data

    @staticmethod
    def delete(product_id):
        try:
            product = ProductRepository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        ProductRepository.delete(product_id)


class ProductCategoryService:

    @staticmethod
    def get():
        categories = ProductCategoryRepository.get()
        serializer = ProductCategorySerializer(categories, many=True)
        return serializer.data

    @staticmethod
    def get_by_id(category_id):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        serializer = ProductCategorySerializer(category)
        return serializer.data

    @staticmethod
    def create(data):
        serializer = ProductCategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.validated_data
            ProductCategoryRepository.create(category)
        else:
            raise CategoryValidationException(errors=serializer.errors)
        return serializer.data

    @staticmethod
    def update(category_id, data):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        serializer = ProductCategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            category = serializer.validated_data
            ProductCategoryRepository.update(category_id, category)
        else:
            raise CategoryValidationException(category_id, serializer.errors)
        return serializer.data

    @staticmethod
    def delete(category_id):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        ProductCategoryRepository.delete(category_id)
