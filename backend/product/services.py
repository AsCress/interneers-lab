from .exceptions import CategoryNotFoundError, ProductNotFoundError
from .models import Product, ProductCategory
from .serializers import ProductSerializer
from .serializers import ProductCategorySerializer
from .repository import ProductRepository
from .repository import ProductCategoryRepository


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
        except Product.DoesNotExist:
            raise ProductNotFoundError()
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
        return [serializer.data, serializer.errors]

    @staticmethod
    def update(product_id, data):
        try:
            product = ProductRepository.get_product(product_id)
        except Product.DoesNotExist:
            raise ProductNotFoundError()
        serializer = ProductSerializer(product, data, partial=True)
        if serializer.is_valid():
            product = serializer.validated_data
            ProductRepository.update(product_id, product)
        return [serializer.data, serializer.errors]

    @staticmethod
    def delete(product_id):
        try:
            product = ProductRepository.get_product(product_id)
        except Product.DoesNotExist:
            raise ProductNotFoundError()
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
        except ProductCategory.DoesNotExist:
            raise CategoryNotFoundError()
        serializer = ProductCategorySerializer(category)
        return serializer.data

    @staticmethod
    def create(data):
        serializer = ProductCategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.validated_data
            ProductCategoryRepository.create(category)
        return [serializer.data, serializer.errors]

    @staticmethod
    def update(category_id, data):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except ProductCategory.DoesNotExist:
            raise CategoryNotFoundError()
        serializer = ProductCategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            category = serializer.validated_data
            ProductCategoryRepository.update(category_id, category)
        return [serializer.data, serializer.errors]

    @staticmethod
    def delete(category_id):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except ProductCategory.DoesNotExist:
            raise CategoryNotFoundError()
        ProductCategoryRepository.delete(category_id)

    @staticmethod
    def add_to_category(category_id, product_ids):
        try:
            category = ProductCategoryRepository.get_category(category_id)
        except ProductCategory.DoesNotExist:
            raise CategoryNotFoundError()

        for product_id in product_ids:
            try:
                product = ProductRepository.get_product(product_id)
            except Product.DoesNotExist:
                raise ProductNotFoundError(f"Product not found: {product_id}")
            ProductRepository.update(product.id, {"category": category})

    @staticmethod
    def remove_from_category(category_id, product_ids):
        uncategorized_category = ProductCategoryRepository.get_by_title(
            title="Uncategorized"
        )

        try:
            category = ProductCategoryRepository.get_category(category_id)
        except ProductCategory.DoesNotExist:
            raise CategoryNotFoundError()

        products_to_update = []
        for product_id in product_ids:
            try:
                product = ProductRepository.get_product(product_id)
            except Product.DoesNotExist:
                raise ProductNotFoundError(f"Product not found: {product_id}")
            if product.category != category:
                raise ProductNotFoundError(f"Product not in category: {product_id}")
            products_to_update.append(product)

        for product in products_to_update:
            ProductRepository.update(product.id, {"category": uncategorized_category})
