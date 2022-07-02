"""Define models for Fifa Manager"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from manager.submodels.base_models import (
    AttributeCategory,
    BaseEmployee,
    BaseModel,
    BaseStatus,
    Country,
)
from manager.submodels.user_models import Manager


UserModel = get_user_model()

class PlayerPosition(BaseModel):
    position = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.position

class ContractType(BaseModel):
    service = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.service

class TransferStatus(BaseStatus):
    pass

class PlayerStatus(BaseStatus):
    pass

class OfferStatus(BaseStatus):
    pass

class OfferType(BaseModel):
    type = models.CharField(
        max_length=settings.MAX_LENGTH,
        unique=True,
        null=False,
        editable=False,
    )

    def __str__(self):
        return self.type

class League(BaseModel):
    country = models.ForeignKey(
        to=Country,
        null=False,
        on_delete=models.CASCADE,
    )
    division = models.IntegerField()

class Team(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH)
    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        editable=False,
    )
    manager = models.ForeignKey(
        to=Manager,
        null=True,
        on_delete=models.SET_NULL,
    )
    budget = models.PositiveBigIntegerField(default=settings.DEFAULT_BUDGET, editable=False)
    league = models.ForeignKey(
        to=League,
        null=False,
        on_delete=models.CASCADE,
    )
    value = models.PositiveBigIntegerField(default=settings.DEFAULT_VALUE, editable=False)
    has_manager = models.BooleanField(default=False)
    starting_manager_salary = models.PositiveBigIntegerField()
    existing = models.BooleanField(default=True, null=False)

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
    contract_type = models.ForeignKey(
        to=ContractType,
        null=False,
        on_delete=models.CASCADE,
    )
    join_date = models.DateField()

class BaseOffer(BaseModel):
    asking_price = models.PositiveBigIntegerField()
    offered_price = models.PositiveBigIntegerField()
    player = models.ForeignKey(
        to=Player,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

class Transfer(BaseOffer):
    buyer = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name='buyer_transfers',
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name='seller_transfers',
    )
    status = models.ForeignKey(
        to=TransferStatus,
        null=False,
        on_delete=models.CASCADE,
    )

class CounterOffer(BaseOffer):
    buyer = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name='buyer_offers',
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name='seller_offers',
    )
    status = models.ForeignKey(
        to=OfferStatus,
        null=False,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        to=OfferType,
        null=False,
        on_delete=models.CASCADE,
    )

class BaseNegotiation(BaseModel):
    asking_salary = models.PositiveBigIntegerField()
    offer_salary = models.PositiveBigIntegerField()
    team = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

class PlayerNegotiation(BaseNegotiation):
    player = models.ForeignKey(
        to=Player,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

class ManagerNegotiation(BaseNegotiation):
    manager = models.ForeignKey(
        to=Manager,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

class BaseAttribute(BaseModel):
    player = models.ForeignKey(
        to=Player,
        null=False,
        on_delete=models.CASCADE,
    )
    value = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        to=AttributeCategory,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
