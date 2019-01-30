from django.db import models
from .base_model import BaseModel
from .assessment_type import Assessment
# Create your models here.

class Question(BaseModel):
    mark = models.DecimalField(max_digits=19, decimal_places=10, default=0.0)
    number = models.IntegerField(blank=True, null=True)
    question_text = models.TextField(blank=False, null=False)
    assessments = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    multi_choice = models.BooleanField(default=False)
    image_url = models.CharField(blank=True, max_length=250, null=True)
    
    def assessments_id(self):
        return None

    def __str__(self):
        return self.question_text
