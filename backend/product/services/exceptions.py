from ..serializers import ResponseSerializer
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class MessageResponse:
    def __init__(self, message):
        self.message = message


class ServiceException(APIException):
    product_id = None
    category_id = None
    errors = None


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ServiceException):
            if exc.product_id is not None:
                response.data["product_id"] = exc.product_id
            if exc.category_id is not None:
                response.data["category_id"] = exc.category_id
            if exc.errors is not None:
                response.data["errors"] = exc.errors

    return response


class ProductNotFoundException(ServiceException):
    detail = "Product Not Found"
    status_code = 404

    def __init__(self, product_id):
        self.product_id = product_id


class CategoryNotFoundException(ServiceException):
    detail = "Category Not Found"
    status_code = 404

    def __init__(self, category_id):
        self.category_id = category_id


class ProductValidationException(ServiceException):
    detail = "Product Validation Error"
    status_code = 400

    def __init__(self, product_id=None, errors=None):
        if product_id:
            self.product_id = product_id
        if errors:
            self.errors = errors
        else:
            self.errors = ResponseSerializer(MessageResponse("Invalid Product ID")).data


class CategoryValidationException(ServiceException):
    detail = "Category Validation Error"
    status_code = 400

    def __init__(self, category_id=None, errors=None):
        if category_id:
            self.category_id = category_id
        if errors:
            self.errors = errors
        else:
            self.errors = ResponseSerializer(MessageResponse("Invalid Product ID")).data
