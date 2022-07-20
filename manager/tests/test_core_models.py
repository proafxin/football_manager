"""Test core models"""

import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import crypto
from rest_framework import test

from manager import models

MAX_LENGTH = settings.MAX_LENGTH
DEFAULT_VALUE = settings.DEFAULT_VALUE
DEFAULT_ATTRIBUTE_VALUE = settings.DEFAULT_ATTRIBUTE_VALUE
UserModel = get_user_model()
ATTRIBUTES = settings.ATTRIBUTES


class TestCoreModels(test.APITestCase):
    """Test all core models"""

    def setUp(self):
        """Create each of the core models once at the start of each test"""
        # pylint: disable=no-member
        self.__status = settings.STATUS
        self.__country_names = ["AFGHANISTAN", "INDIA", "BANGLADESH"]
        self.__countries = []
        self.__leagues = []

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
            status=self.__status["player"][0],
            salary=10000,
            position=settings.PLAYER_POSITIONS[0],
            join_date=datetime.datetime.now(),
            price=0,
        )

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
        self.assertEqual(self.__team.num_players, settings.DEFAULT_INITIAL_PLAYER_NUMBER)
        self.assertEqual(self.__team.budget, settings.DEFAULT_BUDGET)
        self.assertEqual(self.__team.value, settings.DEFAULT_VALUE)
        self.assertEqual(self.__team.league, self.__leagues[0])
        self.assertEqual(self.__team.earning, 0)
        self.assertEqual(self.__team.starting_manager_salary, settings.DEFAULT_SALARY)
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
        self.assertEqual(player.status, settings.STATUS["player"][0])
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
        attribute: str = settings.ATTRIBUTES[0]
        category: str = settings.CATEGORIES[0]
        attribute_category = models.AttributeCategory.objects.create(
            attribute=attribute,
            category=category,
        )
        self.assertIsNotNone(attribute_category)
        self.assertEqual(attribute_category.attribute, attribute)
        self.assertEqual(attribute_category.category, category)
        self.assertEqual(str(attribute_category), f"{attribute} {category}")
