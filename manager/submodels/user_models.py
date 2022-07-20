"""Define user related models"""


from django import conf
from django.contrib.auth import models as auth_models
from django.db import models

from manager.submodels import base_models


class UserManager(auth_models.BaseUserManager):
    """User manager model with email and no username"""

    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        """
        Helper to create a User with email and password.

        :param email: Email of the user.
            Must be a valid email.
        :type email: models.EmailField.
        :param password: Password of the user.
        :returns: User created using the email and password and other fields from arguments.
        :rtype: User
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        """
        Create a normal User with email and password.
        Set is_staff and is_superuser to False by default.

        :return: A normal user created using email and password.
        :rtype: User
        """
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """
        Create a super User with email and password.
        Set is_staff and is_superuser to True by default.

        :return: A super user created using email and password.
        :rtype: User
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **kwargs)


class User(auth_models.AbstractUser):
    """User Model with email as username"""

    username = None
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


UserModel = conf.settings.AUTH_USER_MODEL


class Manager(base_models.BasePerson):
    """Define Manager corresponding to User model"""

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        editable=False,
    )
