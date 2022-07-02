"""Define models for Fifa Manager"""

from django.conf import settings
from django.db import models

from manager.models.base_models import (
    BaseModel,
    BaseEmployee,
    UserModel,
)
from manager.models.helper_models import (
    Country,
    PlayerPosition,
    PlayerStatus,
)

class Team(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH)
    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        editable=False,
        related_name='teams',
    )
    budget = models.PositiveBigIntegerField(default=settings.DEFAULT_BUDGET, editable=False)
    country = models.CharField(choices=settings.COUNTRY_CHOICES, max_length=settings.MAX_LENGTH, null=True)
    value = models.PositiveBigIntegerField(default=settings.DEFAULT_VALUE, editable=False)
    starting_manager_salary = models.PositiveBigIntegerField()

class Scout(BaseEmployee):
    experience = models.PositiveIntegerField(max_length=1)
    judgement = models.PositiveIntegerField(max_length=1)

class League(BaseModel):
    country = models.ForeignKey(
        to=Country,
        null=False,
        on_delete=models.CASCADE,
    )
    division = models.IntegerField()

class Player(BaseEmployee):
    team = models.ForeignKey(
        to=Team,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name='players',
    )
    price = models.PositiveBigIntegerField()
    status = models.ForeignKey(
        to=PlayerStatus,
        null=True,
        on_delete=models.SET_NULL,
    )
    position = models.ForeignKey(
        to=PlayerPosition,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

class Negotiation(BaseModel):
    asking_value = models.PositiveBigIntegerField()
    offered_value = models.PositiveBigIntegerField()
    employer_model_name = models.CharField(max_length=settings.MAX_LENGTH)
    employer_id = models.PositiveBigIntegerField()
    employee_model_name = models.CharField(max_length=settings.MAX_LENGTH)
    employee_id = models.PositiveBigIntegerField()
