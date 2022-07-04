"""Define tests for Models"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.crypto import get_random_string

from manager.models import Player


UserModel = get_user_model()

class TestModels(TestCase):
    """Test all models"""

    def setUp(self):
        pass

    def test_normal_user(self):
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
        email = 'test@test.com'
        try:
            UserModel.objects.create_superuser(
                email=email,
                password=get_random_string(length=16),
                is_staff=False,
                is_superuser=True,
            )
        # pylint: disable=broad-exception
        except Exception as exc:
            self.assertIsInstance(exc, ValueError)
        try:
            UserModel.objects.create_superuser(
                email=email,
                password=get_random_string(length=16),
                is_staff=True,
                is_superuser=False,
            )
        # pylint: disable=broad-exception
        except Exception as exc:
            self.assertIsInstance(exc, ValueError)
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

    def test_player(self):
        pass

    def test_team(self):
        pass
