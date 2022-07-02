"""Define base models to inherit later"""

from django.conf import settings
from django.db import models

from manager.models.helper_models import Country


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class  Meta:
        abstract = True

class BasePerson(BaseModel):
    first_name = models.CharField(max_length=settings.MAX_LENGTH, null=True)
    last_name = models.CharField(max_length=settings.MAX_LENGTH, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True

UserModel = settings.AUTH_USER_MODEL

class BaseEmployee(BasePerson):
    salary = models.PositiveBigIntegerField()
    date_of_birth = models.DateField(editable=False, null=False)
    country = models.ForeignKey(
        to=Country,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
