
from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from assessment.middlewares.validators.errors import raises, raises_error

def validate_password(value):  
   if len(value)<4 or not value:
       raises('password_error', 400)

def validate_email(value):
    user = User.objects.filter(email=value)
    if user:
        raises_error('exist', 400, 'Email')
    return value

def get_or_404(model, id):
    exist = model.objects.filter(pk=id)
    if not exist:
        raises('not_found', 404)
