from rest_framework.test import APITestCase
from mongoengine import connect, disconnect
from product.repository.repository import ProductRepository, ProductCategoryRepository
from django.urls import reverse


class ProductTests(APITestCase):
    def setUp(self):
        connect(
            "inventory",
            host="mongodb://root:example@localhost:27018/inventory?authSource=admin",
        )
        self.category = ProductCategoryRepository.create(
            {"title": "Test Category", "description": "Test Description"}
        )
        self.product = ProductRepository.create(
            {
                "name": "Test Product",
                "description": "Test Description",
                "category": self.category.id,
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            }
        )

    def test_get_product(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_product_by_id_valid(self):
        url = reverse("product-list")
        url = url + str(self.product.id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_by_id_invalid(self):
        invalid_id = "67fb3895bfebba6f3882856"
        url = reverse("product-list")
        url = url + invalid_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_product_by_id_not_found(self):
        nonexistent_id = "67fb3895bfebba6f3882856c"
        url = reverse("product-list")
        url = url + nonexistent_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_product_by_category(self):
        url = reverse("product-list")
        url = url + "?category_id=" + str(self.category.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_product_valid(self):
        url = reverse("product-list")
        data = {
            "name": "New Product",
            "description": "New Description",
            "category": str(self.category.id),
            "price": 20000,
            "brand": "New Brand",
            "quantity": 50,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_product_missing_fields(self):
        url = reverse("product-list")
        products = [
            {
                "name": "New Product",
                "description": "New Description",
                "category": str(self.category.id),
                "price": 20000,
                "brand": "New Brand",
            },
            {
                "name": "New Product",
                "description": "New Description",
                "category": str(self.category.id),
                "price": 20000,
                "quantity": 50,
            },
            {
                "name": "New Product",
                "description": "New Description",
                "category": str(self.category.id),
                "brand": "New Brand",
                "quantity": 50,
            },
            {
                "name": "New Product",
                "description": "New Description",
                "price": 20000,
                "brand": "New Brand",
                "quantity": 50,
            },
            {
                "description": "New Description",
                "category": str(self.category.id),
                "price": 20000,
                "brand": "New Brand",
                "quantity": 50,
            },
        ]
        for product in products:
            response = self.client.post(url, product, format="json")
            self.assertEqual(response.status_code, 400)

    def test_create_product_invalid(self):
        url = reverse("product-list")
        products = [
            {
                "name": "New Product",
                "description": "New Description",
                "category": str(self.category.id),
                "price": -1,
                "brand": "New Brand",
                "quantity": -1,
            },
            {
                "name": "New Product",
                "description": "New Description",
                "category": str(self.category.id),
                "price": -1,
                "brand": "New Brand",
                "quantity": 50,
            },
            {
                "name": "New Product",
                "description": "New Description",
                "category": "67fb3895bfebba6f3882856c",
                "price": 10000,
                "brand": "New Brand",
                "quantity": 10,
            },
            {
                "name": "New Product",
                "description": "New Description",
                "category": "67fb3895bfebba6f3882856",
                "price": 10000,
                "brand": "New Brand",
                "quantity": 10,
            },
        ]
        for product in products:
            response = self.client.post(url, product, format="json")
            self.assertEqual(response.status_code, 400)

    def test_update_product_valid(self):
        url = reverse("product-list")
        url = url + str(self.product.id) + "/"
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "category": str(self.category.id),
            "price": 15000,
            "brand": "Updated Brand",
            "quantity": 80,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_product_invalid(self):
        url = reverse("product-list")
        url = url + str(self.product.id) + "/"
        products = [
            {
                "name": "Updated Product",
                "description": "Updated Description",
                "category": str(self.category.id),
                "price": 10000,
                "brand": "Updated Brand",
                "quantity": -1,
            },
            {
                "name": "Updated Product",
                "description": "Updated Description",
                "category": "67fb3895bfebba6f3882856c",
                "price": -1,
                "brand": "Updated Brand",
                "quantity": 80,
            },
            {
                "name": "Updated Product",
                "description": "Updated Description",
                "category": str(self.category.id),
                "price": 15000,
                "brand": "",
                "quantity": 80,
            },
            {
                "name": "",
                "description": "Updated Description",
                "category": str(self.category.id),
                "price": 15000,
                "brand": "Updated Brand",
                "quantity": 80,
            },
            {
                "name": "Updated Product",
                "description": "",
                "category": str(self.category.id),
                "price": 15000,
                "brand": "Updated Brand",
                "quantity": 80,
            },
        ]
        for product in products:
            response = self.client.put(url, product, format="json")
            self.assertEqual(response.status_code, 400)

    def test_update_product_not_found(self):
        url = reverse("product-list")
        nonexistent_id = "67fb3895bfebba6f3882856c"
        url = url + nonexistent_id + "/"
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "category": str(self.category.id),
            "price": 15000,
            "brand": "Updated Brand",
            "quantity": 80,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_delete_product_valid(self):
        product = ProductRepository.create(
            {
                "name": "Test Product",
                "description": "Test Description",
                "category": self.category.id,
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            }
        )
        url = reverse("product-list")
        url = url + str(product.id) + "/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_product_not_found(self):
        url = reverse("product-list")
        nonexistent_id = "67fb3895bfebba6f3882856c"
        url = url + nonexistent_id + "/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        ProductRepository.delete(self.product.id)
        ProductCategoryRepository.delete(self.category.id)
        disconnect()
