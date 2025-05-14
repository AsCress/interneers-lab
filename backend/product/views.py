from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.services import ProductService
from .services.services import ProductCategoryService
from rest_framework.pagination import PageNumberPagination
from .serializers import ResponseSerializer
from .services.exceptions import MessageResponse


# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductCreateView(APIView):
    pagination_class = ProductPagination
    product_service = ProductService()
    category_service = ProductCategoryService()

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(data, self.request, view=self)
        return paginator.get_paginated_response(results)

    def list(self, request):
        products = self.product_service.get()
        return self.get_paginated_response(products)

    def list_by_category(self, request, category_id):
        products = self.product_service.get_by_category(category_id)
        return self.get_paginated_response(products)

    def get(self, request):
        category_id = request.GET.get("category_id")
        if category_id:
            self.category_service.get_by_id(category_id)
            return self.list_by_category(request, category_id)
        return self.list(request)

    def post(self, request):
        product = self.product_service.create(request.data)
        return Response(product, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    product_service = ProductService()
    category_service = ProductCategoryService()

    def get_by_id(self, product_id):
        product = self.product_service.get_by_id(product_id)
        return Response(product, status=status.HTTP_200_OK)

    def get(self, request, product_id=None):
        if product_id:
            return self.get_by_id(product_id)

    def put(self, request, product_id):
        product = self.product_service.update(product_id, request.data)
        return Response(product, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        self.product_service.delete(product_id)
        return Response(
            ResponseSerializer(MessageResponse("Product deleted successfully")).data,
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductCategoryCreateView(APIView):
    pagination_class = ProductPagination
    product_service = ProductService()
    category_service = ProductCategoryService()

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(data, self.request, view=self)
        return paginator.get_paginated_response(results)

    def list(self, request):
        categories = self.category_service.get()
        return self.get_paginated_response(categories)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        category = self.category_service.create(request.data)
        return Response(category, status=status.HTTP_201_CREATED)


class ProductCategoryDetailView(APIView):
    pagination_class = ProductPagination
    product_service = ProductService()
    category_service = ProductCategoryService()

    def get_by_id(self, category_id):
        category = self.category_service.get_by_id(category_id)
        return Response(category, status=status.HTTP_200_OK)

    def get(self, request, category_id=None):
        if category_id:
            return self.get_by_id(category_id)

    def post(self, request, category_id=None):
        if request.path.endswith("/products/"):
            return self.add_to_category(request, category_id)

    def put(self, request, category_id):
        category = self.category_service.update(category_id, request.data)
        return Response(category, status=status.HTTP_200_OK)

    def delete(self, request, category_id):
        if request.path.endswith("/products/"):
            return self.remove_from_category(request, category_id)
        self.category_service.delete(category_id)
        return Response(
            ResponseSerializer(MessageResponse("Category deleted successfully")).data,
            status=status.HTTP_204_NO_CONTENT,
        )

    def add_to_category(self, request, category_id):
        if not isinstance(request.data, list):
            return Response(
                ResponseSerializer(
                    MessageResponse("Request data must be a list of product IDs")
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.category_service.add_to_category(category_id, request.data)

        return Response(
            ResponseSerializer(
                MessageResponse("Products added to category successfully")
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def remove_from_category(self, request, category_id):
        if not isinstance(request.data, list):
            return Response(
                ResponseSerializer(
                    MessageResponse("Request data must be a list of product IDs")
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.category_service.remove_from_category(category_id, request.data)

        return Response(
            ResponseSerializer(
                MessageResponse("Products removed from category successfully")
            ).data,
            status=status.HTTP_201_CREATED,
        )
