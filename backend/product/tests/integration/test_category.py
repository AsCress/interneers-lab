from rest_framework.test import APITestCase
from mongoengine import connect, disconnect
from product.repository.repository import ProductRepository, ProductCategoryRepository
from django.urls import reverse


class CategoryTests(APITestCase):
    def setUp(self):
        connect(
            "inventory",
            host="mongodb://root:example@localhost:27018/inventory?authSource=admin",
        )
        self.product = ProductRepository.create(
            {
                "name": "Test Product",
                "description": "Test Description",
                "category": "67f90795d97427e5fa53f640",
                "price": 10000,
                "brand": "Test Brand",
                "quantity": 100,
            }
        )
        self.category = ProductCategoryRepository.create(
            {"title": "Test Category", "description": "Test Description"}
        )

    def test_get_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_category_by_id_valid(self):
        url = reverse("category-list") + str(self.category.id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_category_by_id_invalid(self):
        invalid_id = "67fb3895bfebba6f3882856"
        url = reverse("category-list") + invalid_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_category_by_id_not_found(self):
        non_existent_id = "67fb3895bfebba6f3882856c"
        url = reverse("category-list") + non_existent_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_category_valid(self):
        url = reverse("category-list")
        data = {
            "title": "New Category",
            "description": "New Description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_category_missing_fields(self):
        url = reverse("category-list")
        categories = [
            {
                "description": "New Description",
            },
            {
                "title": "New Category",
            },
        ]
        for data in categories:
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, 400)

    def test_create_category_invalid(self):
        url = reverse("category-list")
        data = {
            "title": "",
            "description": "New Description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_category_valid(self):
        url = reverse("category-list") + str(self.category.id) + "/"
        data = {
            "title": "Updated Category",
            "description": "Updated Description",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_category_invalid(self):
        url = reverse("category-list") + str(self.category.id) + "/"
        data = {
            "title": "",
            "description": "Missing title",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_category_not_found(self):
        non_existent_id = "67fb3895bfebba6f3882856c"
        url = reverse("category-list") + non_existent_id + "/"
        data = {
            "title": "Doesn't exist",
            "description": "Not found",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_delete_category_valid(self):
        category = ProductCategoryRepository.create(
            {"title": "Newer Category", "description": "New Description"}
        )
        url = reverse("category-list") + str(category.id) + "/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_category_not_found(self):
        url = reverse("category-list") + "67fb3895bfebba6f3882856c" + "/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_add_to_category_valid(self):
        url = reverse("category-list") + str(self.category.id) + "/products/"
        data = [str(self.product.id)]
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_add_to_category_invalid(self):
        url = reverse("category-list") + str(self.category.id) + "/products/"
        data = ["67f90795d97427e5fa53f64"]
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_add_to_category_not_found(self):
        url = reverse("category-list") + "67fb3895bfebba6f3882856c" + "/products/"
        data = ["67f90795d97427e5fa53f641"]
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_remove_from_category_valid(self):
        url = reverse("category-list") + str(self.category.id) + "/products/"
        data = [str(self.product.id)]
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_remove_from_category_invalid(self):
        url = reverse("category-list") + str(self.category.id) + "/products/"
        data = ["67f90795d97427e5fa53f64"]
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_remove_from_category_not_found(self):
        url = reverse("category-list") + "67fb3895bfebba6f3882856c" + "/products/"
        data = ["67f90795d97427e5fa53f641"]
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        ProductRepository.delete(self.product.id)
        ProductCategoryRepository.delete(self.category.id)
        disconnect()
