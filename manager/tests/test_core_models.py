"""Test core models"""

from django.conf import settings
from rest_framework.test import APITestCase

from manager.models import (
    PlayerPosition,
    ContractType,
)


MAX_LENGTH = settings.MAX_LENGTH

class TestCoreModels(APITestCase):
    """Test all core models"""

    def setUp(self):
        """Create each of the core models once at the start of each test"""
        self.__position = 'DEFENDER'
        # pylint: disable=no-member
        self.__player_position = PlayerPosition.objects.create(position=self.__position)
        self.__service = 'FREE AGENT'
        # pylint: disable=no-member
        self.__contract_type = ContractType.objects.create(service=self.__service)

    def test_player_position(self):
        """Test PlayerPosition"""
        self.assertIsNotNone(self.__player_position)
        # pylint: disable=no-member
        self.assertEqual(PlayerPosition.objects.count(), 1)
        self.assertEqual(self.__player_position.position, self.__position)
        self.assertEqual(str(self.__player_position), self.__position)

    def test_contract_type(self):
        """Test ContractType"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(ContractType._meta.get_field('service').max_length, MAX_LENGTH)
        self.assertIsNotNone(self.__contract_type)
        # pylint: disable=no-member
        self.assertEqual(ContractType.objects.count(), 1)
        self.assertEqual(self.__contract_type, ContractType.objects.first())
        self.assertEqual(str(self.__contract_type), self.__service)
        self.assertEqual(self.__contract_type.service, self.__service)
