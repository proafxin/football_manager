"""Define base models to inherit later"""

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class  Meta:
        abstract = True

class Country(BaseModel):
    name = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

class BasePerson(BaseModel):
    first_name = models.CharField(max_length=settings.MAX_LENGTH, null=True)
    last_name = models.CharField(max_length=settings.MAX_LENGTH, null=True)
    date_of_birth = models.DateField(editable=False, null=False)
    country = models.ForeignKey(
        to=Country,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True

class BaseEmployee(BasePerson):
    salary = models.PositiveBigIntegerField()

    class Meta:
        abstract = True

class BaseStatus(BaseModel):
    status = models.CharField(max_length=settings.MAX_LENGTH, unique=True)

    def __str__(self):
        return self.status
    
    class Meta:
        abstract = True
