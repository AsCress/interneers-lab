from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.http import Http404
from .services import ProductService
from mongoengine.errors import DoesNotExist

# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductView(APIView):
    pagination_class = ProductPagination

    def get_product(self, product_id):
        try:
            product = ProductService.get_product(product_id)
        except DoesNotExist:
            raise Http404("Product does not exist")
        return product

    def get(self, request, product_id=None):
        if product_id:
            product = self.get_product(product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = ProductService.get()
        serializer = ProductSerializer(products, many=True)
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(serializer.data, request, view=self)
        return paginator.get_paginated_response(results)
    
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
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)