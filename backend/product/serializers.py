from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Product
from .models import ProductCategory
from rest_framework import serializers


class ProductSerializer(DocumentSerializer):
    class Meta:
        model = Product


class ProductCategorySerializer(DocumentSerializer):
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = ProductCategory


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)
