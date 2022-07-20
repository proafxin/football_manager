"""Define all Manager serializers here"""

from django import conf
from django.contrib.auth import get_user_model
from rest_framework import serializers

from manager import models

UserModel = get_user_model()
ATTRIBUTES: list[str] = conf.settings.ATTRIBUTES
CATEGORIES: list[str] = conf.settings.CATEGORIES


class UserSerializer(serializers.ModelSerializer):
    """Serialize User"""

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def create(self, validated_data):
        """Create user from  valid data"""
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user

    # pylint: disable=too-few-public-methods
    class Meta:
        """Serialize fields for registration"""

        model = UserModel
        fields = ("id", "email", "password")


class ManagerSerializer(serializers.ModelSerializer):
    """Serialize Manager fields"""

    class Meta:
        """Specify fields to serialize"""

        model = models.Manager
        fields = "__all__"


class AttributeCategorySerializer(serializers.ModelSerializer):
    """Serialize AttributeCategory fields"""

    class Meta:
        """Specify fields to serialize"""

        model = models.AttributeCategory
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    """Serialize Country fields"""

    class Meta:
        """Specify fields to serialize"""

        model = models.Country
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    """Serialize League fields"""

    class Meta:
        """Specify fields to serialize"""

        model = models.League
        fields = "__all__"
