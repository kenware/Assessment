
from django.db import models
from .base_model import BaseModel

import datetime

class Assessment(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    total_mark = models.DecimalField(max_digits=19, decimal_places=10, default=0.0)
    max_time = models.TimeField(default=datetime.time(0,59))
    multi_times = models.BooleanField(default=False)

    def __str__(self):
        return self.title
