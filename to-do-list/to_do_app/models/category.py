from django.db import models
from .base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name
