
from django.db import models
from datetime import datetime
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(blank=True, max_length=250)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
