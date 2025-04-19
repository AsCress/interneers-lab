from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import CategoryNotFoundError, ProductNotFoundError
from .services import ProductService
from .services import ProductCategoryService
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductView(APIView):
    pagination_class = ProductPagination

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(data, self.request, view=self)
        return paginator.get_paginated_response(results)

    def get_by_id(self, product_id):
        try:
            product = ProductService.get_by_id(product_id)
        except ProductNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(product, status=status.HTTP_200_OK)

    def list(self, request):
        products = ProductService.get()
        return self.get_paginated_response(products)

    def list_by_category(self, request, category_id):
        products = ProductService.get_by_category(category_id)
        return self.get_paginated_response(products)

    def get(self, request, product_id=None):
        if product_id:
            return self.get_by_id(product_id)
        category_id = request.GET.get("category_id")
        if category_id:
            try:
                ProductCategoryService.get_by_id(category_id)
            except CategoryNotFoundError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            return self.list_by_category(request, category_id)
        return self.list(request)

    def post(self, request):
        product, errors = ProductService.create(request.data)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(product, status=status.HTTP_201_CREATED)

    def put(self, request, product_id):
        try:
            product, errors = ProductService.update(product_id, request.data)
        except ProductNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(product, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            ProductService.delete(product_id)
        except ProductNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductCategoryView(APIView):
    pagination_class = ProductPagination

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(data, self.request, view=self)
        return paginator.get_paginated_response(results)

    def get_by_id(self, category_id):
        try:
            category = ProductCategoryService.get_by_id(category_id)
        except CategoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(category, status=status.HTTP_200_OK)

    def list(self, request):
        categories = ProductCategoryService.get()
        return self.get_paginated_response(categories)

    def get(self, request, category_id=None):
        if category_id:
            return self.get_by_id(category_id)
        return self.list(request)

    def post(self, request, category_id=None):
        if request.path.endswith("/products/"):
            return self.add_to_category(request, category_id)
        category, errors = ProductCategoryService.create(request.data)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(category, status=status.HTTP_201_CREATED)

    def put(self, request, category_id):
        try:
            category, errors = ProductCategoryService.update(category_id, request.data)
        except CategoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(category, status=status.HTTP_201_CREATED)

    def delete(self, request, category_id):
        if request.path.endswith("/products/"):
            return self.remove_from_category(request, category_id)
        try:
            ProductCategoryService.delete(category_id)
        except CategoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def add_to_category(self, request, category_id):
        if not isinstance(request.data, list):
            return Response(
                {"error": "Request data must be a list of product IDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ProductCategoryService.add_to_category(category_id, request.data)
        except (CategoryNotFoundError, ProductNotFoundError) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Products added to category successfully"},
            status=status.HTTP_201_CREATED,
        )

    def remove_from_category(self, request, category_id):
        if not isinstance(request.data, list):
            return Response(
                {"error": "Request data must be a list of product IDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ProductCategoryService.remove_from_category(category_id, request.data)
        except (CategoryNotFoundError, ProductNotFoundError) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Products removed from category successfully"},
            status=status.HTTP_201_CREATED,
        )
