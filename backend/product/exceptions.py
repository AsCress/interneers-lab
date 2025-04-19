class ProductNotFoundError(Exception):
    def __init__(self, message="Product not found"):
        self.response = {"error": message}
        super().__init__(message)


class CategoryNotFoundError(Exception):
    def __init__(self, message="Category not found"):
        self.response = {"error": message}
        super().__init__(message)
