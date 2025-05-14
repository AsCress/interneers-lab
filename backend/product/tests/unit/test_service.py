import unittest
from unittest.mock import patch
from product.services.services import ProductService
import django.test
from product.services.exceptions import ProductNotFoundException
from product.repository.exceptions import ProductDoesNotExist
from product.services.exceptions import ProductValidationException


class TestProductService(django.test.TestCase):
    @patch("product.services.services.ProductRepository")
    def setUp(self, mock_product_repository):
        self.product_service = ProductService()
        self.product_service.product_repository = mock_product_repository

    @patch("product.services.services.ProductSerializer")
    def test_get(self, mock_product_serializer):
        self.product_service.product_repository.get.return_value = []
        mock_product_serializer.return_value.data = []
        data = self.product_service.get()
        self.assertIsInstance(data, list)

    @patch("product.services.services.ProductSerializer")
    def test_get_by_id(self, mock_product_serializer):
        mock_product = {
            "id": "67e8ef6bd739b2427101bddc",
            "name": "Test Product",
            "description": "Test Description",
            "category": "67f90795d97427e5fa53f640",
            "price": 10000,
            "brand": "Test Brand",
            "quantity": 100,
        }
        self.product_service.product_repository.get_product.return_value = mock_product
        mock_product_serializer.return_value.data = mock_product
        data = self.product_service.get_by_id("67e8ef6bd739b2427101bddc")
        self.assertEqual(data, mock_product)

    @patch("product.services.services.ProductSerializer")
    def test_get_by_id_not_found(self, mock_product_serializer):
        self.product_service.product_repository.get_product.side_effect = (
            ProductDoesNotExist
        )
        mock_product_serializer.return_value.data = None
        with self.assertRaises(ProductNotFoundException):
            self.product_service.get_by_id("67e8ef6bd739b2427101bddc")

    @patch("product.services.services.ProductSerializer")
    def test_get_by_category(self, mock_product_serializer):
        mock_product = [
            {
                "id": "67e8ef6bd739b2427101bddc",
                "name": "Test Product",
                "description": "Test Description",
                "category": "67f90795d97427e5fa53f640",
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            }
        ]
        self.product_service.product_repository.get_by_category.return_value = (
            mock_product
        )
        mock_product_serializer.return_value.data = mock_product
        data = self.product_service.get_by_category("67f90795d97427e5fa53f640")
        self.assertEqual(data, mock_product)

    @patch("product.services.services.ProductSerializer")
    def test_create_valid(self, mock_product_serializer):
        mock_product = {
            "id": "67e8ef6bd739b2427101bddc",
            "name": "Test Product",
            "description": "Test Description",
            "category": "67f90795d97427e5fa53f640",
            "price": 10000,
            "brand": "Test Brand",
            "quantity": 100,
        }
        self.product_service.product_repository.create.return_value = mock_product
        mock_product_serializer.return_value.data = mock_product
        data = self.product_service.create(mock_product)
        self.assertEqual(data, mock_product)

    @patch("product.services.services.ProductSerializer")
    def test_create_invalid(self, mock_product_serializer):
        mock_products = [
            {
                "description": "Test Description",
                "category": "67f90795d97427e5fa53f640",
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            },
            {
                "name": "Test Product",
                "description": "Test Description",
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            },
            {
                "name": "Test Product",
                "description": "Test Description",
                "category": "67f90795d97427e5fa53f640",
                "brand": "Test Brand",
                "quantity": -1,
            },
            {
                "name": "Test Product",
                "description": "Test Description",
                "category": "67f90795d97427e5fa53f640",
                "price": -1,
                "quantity": 100,
            },
        ]
        for mock_product in mock_products:
            mock_product_serializer.return_value.is_valid.return_value = False
            mock_product_serializer.return_value.data = []
            with self.assertRaises(ProductValidationException):
                self.product_service.create(mock_product)

    @patch("product.services.services.ProductSerializer")
    def test_update_valid(self, mock_product_serializer):
        mock_product = {
            "id": "67e8ef6bd739b2427101bddc",
            "name": "Test Product",
            "description": "Test Description",
            "category": "67f90795d97427e5fa53f640",
            "price": 10000,
            "brand": "Test Brand",
            "quantity": 100,
        }
        self.product_service.product_repository.update.return_value = mock_product
        mock_product_serializer.return_value.data = mock_product
        data = self.product_service.update("67e8ef6bd739b2427101bddc", mock_product)
        self.assertEqual(data, mock_product)

    @patch("product.services.services.ProductSerializer")
    def test_update_invalid(self, mock_product_serializer):
        mock_product = {
            "id": "67e8ef6bd739b2427101bddc",
            "name": "Test Product",
            "description": "Test Description",
            "category": "67f90795d97427e5fa53f640",
            "price": -1,
            "brand": "Test Brand",
            "quantity": 100,
        }
        mock_product_serializer.return_value.is_valid.return_value = False
        mock_product_serializer.return_value.data = []
        with self.assertRaises(ProductValidationException):
            self.product_service.update("67e8ef6bd739b2427101bddc", mock_product)

    if __name__ == "__main__":
        unittest.main(verbosity=2)
