"""Define base models to inherit later"""

from django import conf
from django.db import models

MAX_LENGTH = conf.settings.MAX_LENGTH


class BaseModel(models.Model):
    """Abstract model for other models to inherit"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Abstract base class for models"""

        abstract = True


class Country(BaseModel):
    """
    Country model
    """

    name = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        return str(self.name)


class BasePerson(BaseModel):
    """
    BasePerson model
    """

    first_name = models.CharField(max_length=MAX_LENGTH, null=True)
    last_name = models.CharField(max_length=MAX_LENGTH, null=True)
    date_of_birth = models.DateField(editable=False, null=False)
    country = models.ForeignKey(
        to=Country,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """
        Return the human readable name for BasePerson.
        """
        return f"{self.first_name} {self.last_name}"

    # pylint: disable=too-few-public-methods
    class Meta:
        """Make BasePerson abstract."""

        abstract = True


class BaseEmployee(BasePerson):
    """Add salary for an employee"""

    salary = models.PositiveBigIntegerField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """Make BaseEmployee abstract"""

        abstract = True


class BaseStatus(BaseModel):
    """Define abstract status model"""

    status = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        return str(self.status)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Make BaseStatus abstract"""

        abstract = True
