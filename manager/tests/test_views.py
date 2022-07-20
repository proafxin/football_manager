"""UnitTest for Views"""


from django.conf import settings
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
            first_name="First",
            last_name="Last",
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
        """Test /attribute-categories/"""

        url = reverse("attribute-categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
        data = {
            "attribute": settings.ATTRIBUTES[0],
            "category": settings.CATEGORIES[0],
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
            self.assertLessEqual(len(attribute_category["attribute"]), settings.MAX_LENGTH)
            self.assertLessEqual(len(attribute_category["category"]), settings.MAX_LENGTH)

    def _test_country(self):
        """Test  /countries/"""

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
            self.assertLessEqual(len(country["name"]), settings.MAX_LENGTH)

        return data[0]

    def _test_league(self):
        """Test /leagues/"""

        url = reverse("league-list")
        country = self._test_country()

        params = {
            "name": "League 1",
            "country": country["id"],
            "division": 1,
        }
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        league = response.json()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        fields = list(params.keys())
        fields.extend(["created_at", "updated_at"])
        for _league in data:
            for field in fields:
                self.assertIn(field, _league)
            self.assertLessEqual(len(_league["name"]), settings.MAX_LENGTH)

        return league

    def test_team(self):
        """Test /teams/"""

        url = reverse("team-list")
        manager = self.__admin.id
        league = self._test_league()
        params = {
            "name": "Team 1",
            "league": league["id"],
            "manager": manager,
            "existing": False,
        }
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        team = response.json()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teams = response.json()
        fields = list(params.keys())
        fields.extend(
            [
                "created_at",
                "updated_at",
                "value",
                "earning",
                "has_manager",
                "starting_manager_salary",
                "existing",
                "budget",
                "num_players",
            ]
        )
        for _team in teams:
            for field in fields:
                self.assertIn(field, _team)
            self.assertLessEqual(len(_team["name"]), settings.MAX_LENGTH)
            self.assertEqual(_team["owner"], self.__admin.id)
            self.assertEqual(_team["manager"], manager)

        return team
