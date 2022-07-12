"""Test core models"""

import datetime

from django import conf
from django.contrib.auth import get_user_model
from django.utils import crypto
from rest_framework import test

from manager import models

MAX_LENGTH = conf.settings.MAX_LENGTH
DEFAULT_VALUE = conf.settings.DEFAULT_VALUE
DEFAULT_ATTRIBUTE_VALUE = conf.settings.DEFAULT_ATTRIBUTE_VALUE
UserModel = get_user_model()
ATTRIBUTES = conf.settings.ATTRIBUTES


class TestCoreModels(test.APITestCase):
    """Test all core models"""

    def setUp(self):
        """Create each of the core models once at the start of each test"""
        self.__position = "DEFENDER"
        # pylint: disable=no-member
        self.__player_position = models.PlayerPosition.objects.create(position=self.__position)
        self.__status = {
            "transfer": ["OPEN", "CLOSED"],
            "player": ["FOR SALE", "NOT FOR SALE"],
            "offer": ["ACCEPTED", "REJECTED", "STALLED", "COUNTERED"],
        }
        self.__transfer_status = []
        self.__player_status = []
        self.__offer_status = []
        self.__types_offer = ["BUY", "LOAN"]
        self.__offer_types = []
        self.__country_names = ["AFGHANISTAN", "INDIA", "BANGLADESH"]
        self.__countries = []
        self.__leagues = []

        for status in self.__status["transfer"]:
            # pylint: disable=no-member
            self.__transfer_status.append(models.TransferStatus.objects.create(status=status))
        for status in self.__status["player"]:
            # pylint: disable=no-member
            self.__player_status.append(models.PlayerStatus.objects.create(status=status))
        for status in self.__status["offer"]:
            # pylint: disable=no-member
            self.__offer_status.append(models.OfferStatus.objects.create(status=status))
        for offer_type in self.__types_offer:
            # pylint: disable=no-member
            self.__offer_types.append(models.OfferType.objects.create(type=offer_type))
        for i, name in enumerate(self.__country_names):
            # pylint: disable=no-member
            country = models.Country.objects.create(name=name)
            self.__leagues.append(models.League.objects.create(country=country, division=i))
            self.__countries.append(country)
        self.__user = UserModel.objects.create_user(
            email="test@test.com",
            password=crypto.get_random_string(length=12),
        )
        self.__team_name = "Team Name"
        self.__manager = models.Manager.objects.create(user=self.__user)
        self.__team = models.Team.objects.create(
            name=self.__team_name,
            league=self.__leagues[0],
            owner=self.__user,
            manager=self.__manager,
            has_manager=True,
            starting_manager_salary=10000,
        )
        self.__player = models.Player.objects.create(
            team=self.__team,
            status=self.__player_status[0],
            salary=10000,
            position=self.__player_position,
            join_date=datetime.datetime.now(),
            price=0,
        )

    def test_player_position(self):
        """Test models.PlayerPosition"""
        self.assertIsNotNone(self.__player_position)
        # pylint: disable=no-member
        self.assertEqual(models.PlayerPosition.objects.count(), 1)
        self.assertEqual(self.__player_position.position, self.__position)
        self.assertEqual(str(self.__player_position), self.__position)

    def test_transfer_status(self):
        """Test models.TransferStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.TransferStatus._meta.get_field("status").max_length, MAX_LENGTH)
        for transfer_status, status in zip(self.__transfer_status, self.__status["transfer"]):
            self.assertIsNotNone(transfer_status)
            self.assertEqual(str(transfer_status), status)
            self.assertEqual(transfer_status.status, status)

    def test_player_status(self):
        """Test models.PlayerStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.PlayerStatus._meta.get_field("status").max_length, MAX_LENGTH)
        for player_status, status in zip(self.__player_status, self.__status["player"]):
            self.assertIsNotNone(player_status)
            self.assertEqual(str(player_status), status)
            self.assertEqual(player_status.status, status)

    def test_offer_status(self):
        """Test models.OfferStatus"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.OfferStatus._meta.get_field("status").max_length, MAX_LENGTH)
        for offer_status, status in zip(self.__offer_status, self.__status["offer"]):
            self.assertIsNotNone(offer_status)
            self.assertEqual(str(offer_status), status)
            self.assertEqual(offer_status.status, status)

    def test_offer_type(self):
        """Test models.OfferType"""
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.OfferType._meta.get_field("type").max_length, MAX_LENGTH)
        for offer_type, _type in zip(self.__offer_types, self.__types_offer):
            self.assertIsNotNone(offer_type)
            self.assertEqual(str(offer_type), _type)
            self.assertEqual(offer_type.type, _type)

    def test_league(self):
        """Test models.League"""
        for country, league in zip(self.__countries, self.__leagues):
            self.assertIsNotNone(league)
            self.assertEqual(str(league), "")
            self.assertEqual(league.country, country)
            self.assertIsInstance(league.division, int)

    def test_team(self):
        """Test models.Team"""
        self.assertIsNotNone(self.__team)
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.Team._meta.get_field("name").max_length, MAX_LENGTH)
        self.assertEqual(models.Team.objects.count(), 1)
        self.assertEqual(self.__team.owner, self.__user)
        self.assertEqual(self.__team.manager, self.__manager)
        self.assertEqual(self.__team.has_manager, True)
        self.assertEqual(self.__team.num_players, conf.settings.DEFAULT_INITIAL_PLAYER_NUMBER)
        self.assertEqual(self.__team.budget, conf.settings.DEFAULT_BUDGET)
        self.assertEqual(self.__team.value, conf.settings.DEFAULT_VALUE)
        self.assertEqual(self.__team.league, self.__leagues[0])
        self.assertEqual(self.__team.earning, 0)
        self.assertEqual(self.__team.starting_manager_salary, conf.settings.DEFAULT_SALARY)
        self.assertEqual(str(self.__team), f"{self.__team_name}, {self.__leagues[0]}")

    def test_player(self):
        """Test models.Player"""
        player = self.__player
        self.assertIsNotNone(player)
        self.assertEqual(str(player), f"{player.first_name} {player.last_name}")
        self.assertIsInstance(player.join_date, datetime.date)
        # pylint: disable=no-member, protected-access
        self.assertEqual(models.Player._meta.get_field("first_name").max_length, MAX_LENGTH)
        self.assertEqual(models.Player.objects.count(), 1)
        self.assertEqual(player.team, self.__team)
        self.assertEqual(player.status, self.__player_status[0])
        self.assertEqual(player.position, self.__player_position)
        self.assertEqual(player.price, 0)
        self.assertEqual(player.earning, 0)

        for attribute in ATTRIBUTES:
            self.assertEqual(getattr(player, attribute), DEFAULT_ATTRIBUTE_VALUE)

    def test_attribute_category(self):
        """
        Test attribute cateogry
        """
        self.assertEqual(
            models.AttributeCategory._meta.get_field("attribute").max_length, MAX_LENGTH
        )
        self.assertEqual(
            models.AttributeCategory._meta.get_field("category").max_length, MAX_LENGTH
        )
        attribute: str = "pace"
        category: str = "physique"
        attribute_category = models.AttributeCategory.objects.create(
            attribute=attribute,
            category=category,
        )
        self.assertIsNotNone(attribute_category)
        self.assertEqual(attribute_category.attribute, attribute)
        self.assertEqual(attribute_category.category, category)
        self.assertEqual(str(attribute_category), f"{attribute} {category}")
