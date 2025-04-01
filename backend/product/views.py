from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .models import ProductCategory
from .serializers import ProductSerializer
from .serializers import ProductCategorySerializer
from django.http import Http404
from .services import ProductService
from .services import ProductCategoryService
from mongoengine.errors import DoesNotExist


# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductView(APIView):
    pagination_class = ProductPagination

    def get_product(self, product_id):
        try:
            product = ProductService.get_product(product_id)
        except DoesNotExist:
            raise Http404("Product does not exist")
        return product

    def get_by_id(self, product_id):
        product = self.get_product(product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def list(self, request):
        products = ProductService.get()
        serializer = ProductSerializer(products, many=True)
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(serializer.data, request, view=self)
        return paginator.get_paginated_response(results)

    def get(self, request, product_id=None):
        if product_id:
            return self.get_by_id(product_id)
        return self.list(request)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data
            ProductService.create(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = self.get_product(product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = ProductService.update(product_id, serializer.validated_data)
            return Response(ProductSerializer(self.get_product(product_id)).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_product(product_id)
        ProductService.delete(product_id)
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductCategoryView(APIView):
    pagination_class = ProductPagination

    def get_category(self, category_id):
        try:
            category = ProductCategoryService.get_category(category_id)
        except DoesNotExist:
            raise Http404("Category does not exist")
        return category

    def get_by_id(self, category_id):
        category = self.get_category(category_id)
        serializer = ProductCategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        categories = ProductCategoryService.get()
        serializer = ProductCategorySerializer(categories, many=True)
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(serializer.data, request, view=self)
        return paginator.get_paginated_response(results)

    def get(self, request, category_id=None):
        if category_id:
            return self.get_by_id(category_id)
        return self.list(request)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data
            ProductCategoryService.create(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        category = self.get_category(category_id)
        serializer = ProductCategorySerializer(
            category, data=request.data, partial=True
        )
        if serializer.is_valid():
            category = ProductCategoryService.update(
                category_id, serializer.validated_data
            )
            return Response(
                ProductCategorySerializer(self.get_category(category_id)).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        category = self.category(category_id)
        ProductCategoryService.delete(category_id)
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
