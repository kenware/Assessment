
from django.db import models
from .base_model import BaseModel

import datetime

class AssessmentName(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

