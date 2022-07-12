"""Define all Manager serializers here"""

from django import conf
from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from manager import models, services

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

    def validate(self, attrs):
        """Check attribute and category are from the predefined list"""
        attribute = attrs.get("attribute")
        category = attrs.get("category")
        if attribute not in ATTRIBUTES:
            error = services.get_error(
                message=f"{attribute} not in ATTRIBUTES", status_code=status.HTTP_400_BAD_REQUEST
            )
            raise serializers.ValidationError(detail=error, code=status.HTTP_400_BAD_REQUEST)
        if category not in CATEGORIES:
            error = services.get_error(
                message=f"{category} not in CATEGORIES", status_code=status.HTTP_400_BAD_REQUEST
            )
            raise serializers.ValidationError(detail=error, code=status.HTTP_400_BAD_REQUEST)

        return super().validate(attrs)

    class Meta:
        """Specify fields to serialize"""

        model = models.AttributeCategory
        fields = "__all__"
