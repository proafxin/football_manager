"""Define tests for Base Models"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.submodels.base_models import Country


UserModel = get_user_model()
MAX_LENGTH = settings.MAX_LENGTH

class TestBaseModels(TestCase):
    """Test all base models"""

    def test_country(self):
        """Test Country model"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(Country._meta.get_field('name').max_length, MAX_LENGTH)
        country_name = 'RandomCountry'
        # pylint: disable=no-member
        country = Country.objects.create(
            name=country_name
        )
        # pylint: disable=no-member
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(country.name, country_name)
        self.assertEqual(str(country), country_name)
