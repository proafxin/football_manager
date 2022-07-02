"""Define extra models"""

from django.db import models

from manager.models.base_models import (
    BaseModel,
    settings,
)
from manager.models.core_models import Player


class Country(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

class PlayerPosition(BaseModel):
    position = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.position

class ServiceType(BaseModel):
    service = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

class PlayerStatus(BaseModel):
    status = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

class AttributeCategory(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

class Attribute(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

class AtttributeList(BaseModel):
    attribute = models.ForeignKey(
        to=Attribute,
        null=False,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to=AttributeCategory,
        null=False,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        to=Player,
        null=False,
        on_delete=models.CASCADE,
        related_name='attributes',
    )
