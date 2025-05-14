import re
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from product.views import ProductCreateView
from product.views import ProductDetailView
from product.views import ProductCategoryCreateView
from product.views import ProductCategoryDetailView
from django_app.api.views import hello_name

urlpatterns = [
    path("products/", ProductCreateView.as_view(), name="product-list"),
    path("products/<product_id>/", ProductDetailView.as_view()),
    path("categories/", ProductCategoryCreateView.as_view(), name="category-list"),
    path("categories/<category_id>/", ProductCategoryDetailView.as_view()),
    path("categories/<category_id>/products/", ProductCategoryDetailView.as_view()),
    path("admin/", admin.site.urls),
    path("hello/", hello_name),
]
