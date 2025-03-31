import re
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from product.views import ProductView
from product.views import ProductCategoryView
from django_app.api.views import hello_name

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<product_id>/", ProductView.as_view()),
    path("categories/", ProductCategoryView.as_view()),
    path("categories/<category_id>/", ProductCategoryView.as_view()),
    path("admin/", admin.site.urls),
    path("hello/", hello_name),
]
