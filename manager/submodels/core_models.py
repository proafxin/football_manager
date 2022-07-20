"""Define models for Fifa user_models.Manager"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from manager.submodels import base_models, user_models

UserModel = get_user_model()
MAX_LENGTH = settings.MAX_LENGTH
DEFAULT_ATTRIBUTE_VALUE = settings.DEFAULT_ATTRIBUTE_VALUE


def generate_choices(choices):
    """Generate a tuple of choices from the list of choices"""

    return tuple((choice, choice) for choice in choices)


class League(base_models.BaseModel):
    """League model"""

    name = models.CharField(max_length=MAX_LENGTH, null=True, default="")
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

    name = models.CharField(max_length=MAX_LENGTH, null=True, default="")
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
        default=settings.DEFAULT_INITIAL_PLAYER_NUMBER,
        editable=False,
    )
    budget = models.PositiveBigIntegerField(default=settings.DEFAULT_BUDGET, editable=False)
    league = models.ForeignKey(
        to=League,
        null=False,
        on_delete=models.CASCADE,
    )
    value = models.PositiveBigIntegerField(default=settings.DEFAULT_VALUE, editable=False)
    earning = models.PositiveBigIntegerField(default=0, editable=False)
    has_manager = models.BooleanField(default=False)
    starting_manager_salary = models.PositiveBigIntegerField(default=settings.DEFAULT_SALARY)
    existing = models.BooleanField(default=False, null=False)

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
        related_name="players",
    )
    price = models.PositiveBigIntegerField(default=settings.DEFAULT_VALUE)
    status = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.STATUS["player"]),
    )
    position = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.PLAYER_POSITIONS),
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
        on_delete=models.CASCADE,
        related_name="buyer_transfers",
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        on_delete=models.CASCADE,
        related_name="seller_transfers",
    )
    status = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.STATUS["transfer"]),
    )
    contract = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.CONTRACT_TYPES),
    )


class CounterOffer(BaseOffer):
    """Counter an Offer made"""

    buyer = models.ForeignKey(
        to=Team,
        null=False,
        on_delete=models.CASCADE,
        related_name="buyer_offers",
    )
    seller = models.ForeignKey(
        to=Team,
        null=False,
        on_delete=models.CASCADE,
        related_name="seller_offers",
    )
    status = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.STATUS["offer"]),
    )
    type = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.CONTRACT_TYPES),
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
        on_delete=models.CASCADE,
    )


class AttributeCategory(base_models.BaseModel):
    """Model to map each attribute to a category"""

    attribute = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.ATTRIBUTES),
        unique=True,
    )
    category = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=generate_choices(settings.CATEGORIES),
    )

    def __str__(self):
        return f"{self.attribute}: {self.category}"
