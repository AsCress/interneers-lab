from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Product
from .models import ProductCategory


class ProductSerializer(DocumentSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCategorySerializer(DocumentSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"
