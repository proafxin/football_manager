"""Test core models"""

from __future__ import division
from django.conf import settings
from rest_framework.test import APITestCase

from manager.models import (
    ContractType,
    Country,
    League,
    OfferStatus,
    OfferType,
    PlayerPosition,
    PlayerStatus,
    TransferStatus,
)


MAX_LENGTH = settings.MAX_LENGTH

class TestCoreModels(APITestCase):
    """Test all core models"""
    # pylint: disable=too-many-instance-attributes
    def setUp(self):
        """Create each of the core models once at the start of each test"""
        self.__position = 'DEFENDER'
        # pylint: disable=no-member
        self.__player_position = PlayerPosition.objects.create(position=self.__position)
        self.__service = 'FREE AGENT'
        # pylint: disable=no-member
        self.__contract_type = ContractType.objects.create(service=self.__service)
        self.__status = {
            'transfer': ['OPEN', 'CLOSED'],
            'player': ['FOR SALE', 'NOT FOR SALE'],
            'offer': ['ACCEPTED', 'REJECTED', 'STALLED', 'COUNTERED'],
        }
        self.__transfer_status = []
        self.__player_status = []
        self.__offer_status = []
        self.__types_offer = ['BUY', 'LOAN']
        self.__offer_types = []
        self.__country_names = ['AFGHANISTAN', 'INDIA', 'BANGLADESH']
        self.__countries = []
        self.__leagues = []

        for status in self.__status['transfer']:
            # pylint: disable=no-member
            self.__transfer_status.append(TransferStatus.objects.create(status=status))
        for status in self.__status['player']:
            # pylint: disable=no-member
            self.__player_status.append(PlayerStatus.objects.create(status=status))
        for status in self.__status['offer']:
            # pylint: disable=no-member
            self.__offer_status.append(OfferStatus.objects.create(status=status))
        for offer_type in self.__types_offer:
            # pylint: disable=no-member
            self.__offer_types.append(OfferType.objects.create(type=offer_type))
        for i, name in enumerate(self.__country_names):
            # pylint: disable=no-member
            country = Country.objects.create(name=name)
            self.__leagues.append(League.objects.create(country=country, division=i))
            self.__countries.append(country)

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

    def test_transfer_status(self):
        """Test TransferStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(TransferStatus._meta.get_field('status').max_length, MAX_LENGTH)
        for transfer_status, status in zip(self.__transfer_status, self.__status['transfer']):
            self.assertIsNotNone(transfer_status)
            self.assertEqual(str(transfer_status), status)
            self.assertEqual(transfer_status.status, status)

    def test_player_status(self):
        """Test PlayerStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(PlayerStatus._meta.get_field('status').max_length, MAX_LENGTH)
        for player_status, status in zip(self.__player_status, self.__status['player']):
            self.assertIsNotNone(player_status)
            self.assertEqual(str(player_status), status)
            self.assertEqual(player_status.status, status)

    def test_offer_status(self):
        """Test OfferStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(OfferStatus._meta.get_field('status').max_length, MAX_LENGTH)
        for offer_status, status in zip(self.__offer_status, self.__status['offer']):
            self.assertIsNotNone(offer_status)
            self.assertEqual(str(offer_status), status)
            self.assertEqual(offer_status.status, status)

    def test_offer_type(self):
        """Test OfferType"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(OfferType._meta.get_field('type').max_length, MAX_LENGTH)
        for offer_type, _type in zip(self.__offer_types, self.__types_offer):
            self.assertIsNotNone(offer_type)
            self.assertEqual(str(offer_type), _type)
            self.assertEqual(offer_type.type, _type)

    def test_league(self):
        """Test League"""
        for country, league in zip(self.__countries, self.__leagues):
            self.assertIsNotNone(league)
            self.assertEqual(str(league), '')
            self.assertEqual(league.country, country)
            self.assertIsInstance(league.division, int)
