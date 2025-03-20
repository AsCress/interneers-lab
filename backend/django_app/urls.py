import re
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def format_name(name):
    """Formats the name to remove extra spaces."""
    name = name.strip()
    return re.sub(r'\s+', ' ', name)

def validate_age(age):
    """Validates that the age is a numeric value if provided."""
    if age:
        age = age.strip()
        if not age.isdigit():
            return None
        return int(age)
    return None

def hello_name(request):
    """
    A simple view that returns a greeting message and age in JSON format.
    Uses query parameters named 'name', 'age'.
    """
    name = request.GET.get('name', 'World')
    age = request.GET.get('age')

    age = validate_age(age)
    if age is None and request.GET.get('age'):
        return JsonResponse({'error': 'Age must be a valid number'}, status=400)

    name = format_name(name)

    response = {'message': f'Hello, {name}!'}
    if age is not None:
        response['age'] = age

    return JsonResponse(response)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
]
