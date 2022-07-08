"""Define models for Fifa Manager"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from manager.submodels.base_models import (
    BaseEmployee,
    BaseModel,
    BaseStatus,
    Country,
)
from manager.submodels.user_models import Manager


UserModel = get_user_model()
DEFAULT_ATTRIBUTE_VALUE = settings.DEFAULT_ATTRIBUTE_VALUE

class PlayerPosition(BaseModel):
    """Define different player positions."""
    position = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return str(self.position)

class ContractType(BaseModel):
    """Define different contract types of a player."""
    service = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return str(self.service)

class TransferStatus(BaseStatus):
    """Open or closed"""

class PlayerStatus(BaseStatus):
    """Player for sale or not"""

class OfferStatus(BaseStatus):
    """Countered or Stalled or Accepted or Rejected"""

class OfferType(BaseModel):
    """Buy/Loan"""
    type = models.CharField(
        max_length=settings.MAX_LENGTH,
        unique=True,
        null=False,
        editable=False,
    )

    def __str__(self):
        return str(self.type)

class League(BaseModel):
    """Define the League model"""
    name = models.CharField(max_length=settings.MAX_LENGTH, null=True, default='')
    country = models.ForeignKey(
        to=Country,
        null=False,
        on_delete=models.CASCADE,
    )
    division = models.IntegerField()

    def __str__(self):
        return str(self.name)

class Team(BaseModel):
    """Define the Team model"""
    name = models.CharField(max_length=settings.MAX_LENGTH, null=True, default='')
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
    earning = models.PositiveBigIntegerField(default=0)
    has_manager = models.BooleanField(default=False)
    starting_manager_salary = models.PositiveBigIntegerField()
    existing = models.BooleanField(default=True, null=False)

class Player(BaseEmployee):
    """Define the player model"""
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
    earning = models.PositiveBigIntegerField(default=0)
    salary = models.PositiveBigIntegerField(default=0)
    pace = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    acceleration = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    strength = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    stand_tackle = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    slide_tackle = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    power = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    finishing = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    balance = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    reaction = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    curve = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    freekick = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    positioning = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    vision = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    marking = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    shortpass = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    longpass = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    longshot = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    dribbling = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    ballcontrol = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    heading = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    jumping = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    marking = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    form = models.PositiveSmallIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    morale = models.PositiveBigIntegerField(default=DEFAULT_ATTRIBUTE_VALUE)
    join_date = models.DateField()

class BaseOffer(BaseModel):
    """Define the base offer model"""
    asking_price = models.PositiveBigIntegerField()
    offered_price = models.PositiveBigIntegerField()
    player = models.ForeignKey(
        to=Player,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )
    # pylint: disable=too-few-public-methods
    class Meta:
        """Make BaseOffer abstract"""
        abstract = True

class Transfer(BaseOffer):
    """Define the Transfer model"""
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
    """Counter an Offer made"""
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
    """Define base model for negotiation of an entity with a team"""
    asking_salary = models.PositiveBigIntegerField()
    offer_salary = models.PositiveBigIntegerField()
    team = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )
    # pylint: disable=too-few-public-methods
    class Meta:
        """Make BaseNegotiation abstract"""
        abstract = True

class PlayerNegotiation(BaseNegotiation):
    """Negotiate player salary"""
    player = models.ForeignKey(
        to=Player,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

class ManagerNegotiation(BaseNegotiation):
    """Negotiate manager salary"""
    manager = models.ForeignKey(
        to=Manager,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )

class AttributeCategory(BaseModel):
    """Model to map each attribute to a category"""
    attribute = models.CharField(max_length=settings.MAX_LENGTH, unique=True, null=False)
    category = models.CharField(max_length=settings.MAX_LENGTH, null=False, unique=True)

    def __str__(self):
        return f'{self.attribute} {self.category}'
