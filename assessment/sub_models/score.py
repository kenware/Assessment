from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from .assessment_type import Assessment
from .base_model import BaseModel
# Create your models here.

class Score(BaseModel):
    assessment_score = models.DecimalField(max_digits=19, decimal_places=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessments = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    status = models.CharField(blank=True, max_length=250, default='not started')
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField( blank=True,null=True)
    
    def __str__(self):
        return self.assessment_score

