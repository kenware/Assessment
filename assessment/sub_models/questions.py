from django.db import models
from django.contrib.postgres.fields import ArrayField
from .base_model import BaseModel
from .assessment_type import Assessment
# Create your models here.

class Question(BaseModel):
    mark = models.DecimalField(max_digits=19, decimal_places=10)
    number = models.IntegerField(blank=True, null=True)
    question_text = models.TextField(blank=False, null=False)
    correct_choices = ArrayField(models.IntegerField(), default=[])
    assessments = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    multi_choice = models.BooleanField(default=False)
    image_url = models.CharField(blank=True, max_length=250, null=True)
    
    def assessments_id(self):
        return None

    def __str__(self):
        return self.question_text