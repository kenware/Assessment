from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from .assessment_type import Assessment
from .assessment_name import AssessmentName
from .base_model import BaseModel
# Create your models here.

class Score(BaseModel):
    correct_score = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_name = models.ForeignKey(AssessmentName, on_delete=models.CASCADE)
    assessments = models.ForeignKey(Assessment, on_delete=models.CASCADE) #assessmentType
    status = models.CharField(blank=True, max_length=250, default='started')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField( blank=True,null=True)
    history = JSONField(default={})
    
    def __str__(self):
        return self.status
