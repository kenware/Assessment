
from django.db import models
from datetime import date
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateField(default=date.today())
    updated_at = models.DateField(null=True, blank=True)
    created_by = models.CharField(blank=True, max_length=250)
    deleted_at = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True