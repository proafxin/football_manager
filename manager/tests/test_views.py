"""UnitTest for Views"""


from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status, test

UserModel = get_user_model()


class TestViews(test.APITestCase):
    """Write all tests for views"""

    def setUp(self) -> None:
        password = get_random_string(length=12)
        self.__admin = UserModel.objects.create_user(
            email="admin@test.com",
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        self.client.login(email=self.__admin.email, password=password)
        self.assertEqual(UserModel.objects.count(), 1)
        # self.__country = None

    def test_register(self):
        """Test registration"""

        url = reverse("register")
        data = {
            "email": "test@test.com",
            "password": get_random_string(length=12),
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = response.json()
        self.assertIsNotNone(user)
        self.assertEqual(UserModel.objects.count(), 2)
        self.assertIn("id", user)
        self.assertIn("email", user)
        self.assertEqual(user["email"], data["email"])

    def test_managers(self):
        """Test views.ManagerListView"""

        url = reverse("manager-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        managers = response.json()
        self.assertIsInstance(managers, list)
        for manager in managers:
            self.assertIsInstance(manager, dict)
            fields = ["first_name", "last_name", "user", "country"]
            for field in fields:
                self.assertIn(field, manager)
            self.assertEqual(manager["user"], self.__admin.id)

    def test_attribute_category(self):
        """Test views.AttributeCategoryListView"""

        url = reverse("attribute-categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
        data = {
            "attribute": "pace",
            "category": "physique",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        for attribute_category in data:
            self.assertIsInstance(attribute_category, dict)
            self.assertIn("attribute", attribute_category)
            self.assertIn("category", attribute_category)
            self.assertIsInstance(attribute_category["attribute"], str)
            self.assertIsInstance(attribute_category["category"], str)

    def test_country(self):
        """Test  views.CountryListView"""

        url = reverse("countries")
        country_name = "Bangladesh"
        response = self.client.post(url, data={"name": country_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        country = response.json()
        self.assertIsNotNone(country)
        self.assertIsInstance(country, dict)
        self.assertIn("name", country)
        self.assertEqual(country["name"], country_name)
        # self.__country = country
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        for country in data:
            self.assertIsInstance(country, dict)
            self.assertIn("name", country)
