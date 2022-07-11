"""Define models for Fifa user_models.Manager"""

from django import conf
from django.contrib.auth import get_user_model
from django.db import models

from manager.submodels import base_models, user_models

UserModel = get_user_model()
DEFAULT_ATTRIBUTE_VALUE = conf.settings.DEFAULT_ATTRIBUTE_VALUE


class PlayerPosition(base_models.BaseModel):
    """
    Model for different player positions.

    Must be one of these: ['GOALKEEPER', 'DEFENDER', 'MIDFIELDER', 'ATTACKER']
    """

    position = models.CharField(max_length=conf.settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return str(self.position)


class ContractStatus(base_models.BaseStatus):
    """
    Model for different contract types of a player.

    Must be one of these: ['BUY', 'LOAN']
    """


class TransferStatus(base_models.BaseStatus):
    """
    Model to check if a transfer is open or closed.

    Must be one of these: ['OPEN', 'CLOSED']
    """


class PlayerStatus(base_models.BaseStatus):
    """
    Model to check if a player is for sale or not

    Must be one of these: ['FOR SALE', 'NOT FOR SALE', 'FREE AGENT']
    """


class OfferStatus(base_models.BaseStatus):
    """
    Model to track the current status of an offer.

    Must be one of these: ['ACCEPTED', 'REJECTED', 'STALLED', 'COUNTERED']
    """


class OfferType(base_models.BaseModel):
    """
    Model to track the type of offer made.

    Must be one of these: ['Buy','Loan']
    """

    type = models.CharField(
        max_length=conf.settings.MAX_LENGTH,
        unique=True,
        null=False,
        editable=False,
    )

    def __str__(self):
        return str(self.type)


class League(base_models.BaseModel):
    """League model"""

    name = models.CharField(max_length=conf.settings.MAX_LENGTH, null=True, default="")
    country = models.ForeignKey(
        to=base_models.Country,
        null=False,
        on_delete=models.CASCADE,
    )
    division = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Team(base_models.BaseModel):
    """Team model"""

    name = models.CharField(max_length=conf.settings.MAX_LENGTH, null=True, default="")
    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        editable=False,
    )
    manager = models.ForeignKey(
        to=user_models.Manager,
        null=True,
        on_delete=models.SET_NULL,
    )
    num_players = models.PositiveSmallIntegerField(
        default=conf.settings.DEFAULT_INITIAL_PLAYER_NUMBER,
    )
    budget = models.PositiveBigIntegerField(default=conf.settings.DEFAULT_BUDGET, editable=False)
    league = models.ForeignKey(
        to=League,
        null=False,
        on_delete=models.CASCADE,
    )
    value = models.PositiveBigIntegerField(default=conf.settings.DEFAULT_VALUE, editable=False)
    earning = models.PositiveBigIntegerField(default=0, editable=False)
    has_manager = models.BooleanField(default=False)
    starting_manager_salary = models.PositiveBigIntegerField(conf.settings.DEFAULT_SALARY)
    existing = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}, {self.league}"


class Player(base_models.BaseEmployee):
    """
    Player model
    """

    team = models.ForeignKey(
        to=Team,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="players",
    )
    price = models.PositiveBigIntegerField(default=conf.settings.DEFAULT_VALUE)
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
    earning = models.PositiveBigIntegerField(default=0)
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
    join_date = models.DateField(null=False)


class BaseOffer(base_models.BaseModel):
    """Base offer model for different offer types to inherit."""

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
    """Transfer model"""

    buyer = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name="buyer_transfers",
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name="seller_transfers",
    )
    status = models.ForeignKey(
        to=TransferStatus,
        null=False,
        on_delete=models.CASCADE,
    )
    contract = models.ForeignKey(
        to=ContractStatus,
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
        related_name="buyer_offers",
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
        related_name="seller_offers",
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


class BaseNegotiation(base_models.BaseModel):
    """Abstract base model for negotiation of an entity with a team"""

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
        to=user_models.Manager,
        null=False,
        editable=False,
        on_delete=models.CASCADE,
    )


class AttributeCategory(base_models.BaseModel):
    """Model to map each attribute to a category"""

    attribute = models.CharField(max_length=conf.settings.MAX_LENGTH, unique=True, null=False)
    category = models.CharField(max_length=conf.settings.MAX_LENGTH, null=False)

    def __str__(self):
        return f"{self.attribute} {self.category}"
