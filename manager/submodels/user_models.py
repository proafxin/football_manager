"""Define user related models"""

from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models

from manager.submodels.base_models import BasePerson


class UserManager(BaseUserManager):
    """User manager model with email and no username"""

    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        """
        Helper to create a User with email and password.

        Parameters
        ----------
        email: EmailField
            Email of the user signing up.
        password: str
            Password of the user

        Returns
        -------
        User
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        """
        Create a normal User with email and password.
        Set is_staff and is_superuser to False by default.

        Parameters
        ----------
        email: EmailField
            Email of the user signing up.
        password: str
            Password of the user

        Returns
        -------
        User
        """
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """
        Create a normal User with email and password.
        Set is_staff and is_superuser to True by default.

        Parameters
        ----------
        email: EmailField
            Email of the user signing up.
        password: str
            Password of the user

        Returns
        -------
        User
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **kwargs)

class User(AbstractUser):
    """User Model with email as username"""
    username = None
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

UserModel = settings.AUTH_USER_MODEL

class Manager(BasePerson):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )