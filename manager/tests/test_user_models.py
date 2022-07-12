"""Define tests for Base Models"""

from django import test
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from manager import models

UserModel = get_user_model()


class TestUserModels(test.TestCase):
    """Test all user models"""

    def setUp(self):
        self.__email = "test@test.com"
        self.__password = get_random_string(length=16)
        self.__user = UserModel.objects.create_user(
            email=self.__email,
            password=self.__password,
        )

    def test_normal_user(self):
        """UnitTest normal user creation"""
        self.assertIsNotNone(self.__user)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(self.__user.email, self.__email)
        self.assertEqual(self.__user.is_staff, False)
        self.assertEqual(self.__user.is_superuser, False)
        self.assertEqual(str(self.__user), self.__email)
        self.assertTrue(self.__user.check_password(self.__password))
        self.assertRaises(
            ValueError,
            UserModel.objects.create_user,
            email=None,
            password=get_random_string(length=15),
        )

    def test_superuser(self):
        """UnitTest superuser creation"""
        email = "super@test.com"
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
        self.assertEqual(UserModel.objects.count(), 2)
        self.assertEqual(user.email, email)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_manager(self):
        """UnitTest manager creation"""
        first_name = "First"
        last_name = "Last"
        # pylint: disable=no-member
        manager = models.Manager.objects.create(
            first_name=first_name,
            last_name=last_name,
            user=self.__user,
        )
        self.assertIsNotNone(manager)
        self.assertEqual(models.Manager.objects.count(), 2)
        self.assertEqual(self.__user, manager.user)
        self.assertEqual(manager.first_name, first_name)
        self.assertEqual(manager.last_name, last_name)
        self.assertEqual(str(manager), f"{first_name} {last_name}")
