"""Define tests for Base Models"""

from django import conf, test
from django.contrib.auth import get_user_model

from manager.submodels import base_models

UserModel = get_user_model()
MAX_LENGTH = conf.settings.MAX_LENGTH


class TestBaseModels(test.TestCase):
    """Test all base models"""

    def test_country(self):
        """Test base_models.Country model"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(base_models.Country._meta.get_field("name").max_length, MAX_LENGTH)
        country_name = "Randombase_models.Country"
        # pylint: disable=no-member
        country = base_models.Country.objects.create(name=country_name)
        # pylint: disable=no-member
        self.assertEqual(base_models.Country.objects.count(), 1)
        self.assertEqual(country.name, country_name)
        self.assertEqual(str(country), country_name)
