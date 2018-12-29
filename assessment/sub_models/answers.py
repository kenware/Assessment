
from django.db import models
from .questions import Question
from .base_model import BaseModel
# Create your models here.

class Answer(BaseModel):
    choice_text = models.TextField(blank=False, null=False)
    questions = models.ForeignKey(Question,related_name='answers', on_delete=models.CASCADE)
    image_url =  models.CharField(blank=True, max_length=250)
    
    def __str__(self):
        return self.choice_text