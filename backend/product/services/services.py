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

    def __init__(self):
        self.product_repository = ProductRepository()

    def get(self):
        products = self.product_repository.get()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_by_id(self, product_id):
        try:
            product = self.product_repository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        serializer = ProductSerializer(product)
        return serializer.data

    def get_by_category(self, category_id):
        products = self.product_repository.get_by_category(category_id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def create(self, data):
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.validated_data
            self.product_repository.create(product)
        else:
            raise ProductValidationException(errors=serializer.errors)
        return serializer.data

    def update(self, product_id, data):
        try:
            product = self.product_repository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        serializer = ProductSerializer(product, data, partial=True)
        if serializer.is_valid():
            product = serializer.validated_data
            self.product_repository.update(product_id, product)
        else:
            raise ProductValidationException(product_id, serializer.errors)
        return serializer.data

    def delete(self, product_id):
        try:
            product = self.product_repository.get_product(product_id)
        except ProductDoesNotExist:
            raise ProductNotFoundException(product_id)
        except ProductValidationError:
            raise ProductValidationException(product_id)
        self.product_repository.delete(product_id)


class ProductCategoryService:

    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = ProductCategoryRepository()

    def get(self):
        categories = self.category_repository.get()
        serializer = ProductCategorySerializer(categories, many=True)
        return serializer.data

    def get_by_id(self, category_id):
        try:
            category = self.category_repository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        serializer = ProductCategorySerializer(category)
        return serializer.data

    def create(self, data):
        serializer = ProductCategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.validated_data
            self.category_repository.create(category)
        else:
            raise CategoryValidationException(errors=serializer.errors)
        return serializer.data

    def update(self, category_id, data):
        try:
            category = self.category_repository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        serializer = ProductCategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            category = serializer.validated_data
            self.category_repository.update(category_id, category)
        else:
            raise CategoryValidationException(category_id, serializer.errors)
        return serializer.data

    def delete(self, category_id):
        try:
            category = self.category_repository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)
        self.category_repository.delete(category_id)

    def add_to_category(self, category_id, product_ids):
        try:
            category = self.category_repository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)

        for product_id in product_ids:
            try:
                product = self.product_repository.get_product(product_id)
            except ProductDoesNotExist:
                raise ProductNotFoundException(product_id)
            except ProductValidationError:
                raise ProductValidationException(product_id)

            self.product_repository.update(product.id, {"category": category})

    def remove_from_category(self, category_id, product_ids):
        uncategorized_category = self.category_repository.get_by_title(
            title="Uncategorized"
        )
        try:
            category = self.category_repository.get_category(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFoundException(category_id)
        except CategoryValidationError:
            raise CategoryValidationException(category_id)

        for product_id in product_ids:
            try:
                product = self.product_repository.get_product(product_id)
            except ProductDoesNotExist:
                raise ProductNotFoundException(product_id)
            except ProductValidationError:
                raise ProductValidationException(product_id)

            self.product_repository.update(
                product.id, {"category": uncategorized_category}
            )
