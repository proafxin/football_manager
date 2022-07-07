"""Define tests for Models"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.crypto import get_random_string

from manager.submodels.base_models import Country


UserModel = get_user_model()
MAX_LENGTH = settings.MAX_LENGTH

class TestModels(TestCase):
    """Test all models"""

    def test_normal_user(self):
        """UnitTest normal user creation"""
        email = 'test@test.com'
        user = UserModel.objects.create_user(
            email=email,
            password=get_random_string(length=16),
        )
        self.assertIsNotNone(user)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(user.email, email)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_superuser(self):
        """UnitTest superuser creation"""
        email = 'test@test.com'
        self.assertRaises(
            ValueError,
            UserModel.objects.create_superuser,
            email=email,
            password=get_random_string(length=16),
            is_staff=False,
            is_superuser=True,
        )
        self.assertRaises(
            ValueError,
            UserModel.objects.create_superuser,
            email=email,
            password=get_random_string(length=16),
            is_staff=True,
            is_superuser=False,
        )
        user = UserModel.objects.create_superuser(
            email=email,
            password=get_random_string(length=16),
            is_staff=True,
            is_superuser=True,
        )
        self.assertIsNotNone(user)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(user.email, email)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_country(self):
        """Test Country model"""
        country_name = 'RandomCountry'
        # pylint: disable=no-member
        country = Country.objects.create(
            name=country_name
        )
        # pylint: disable=no-member
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(country.name, country_name)
        self.assertEqual(str(country), country_name)
