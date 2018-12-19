
from rest_framework import serializers
from django.contrib.auth.models import User

from .errors import raises

def validate_password(value):  
   if len(value)<4 or not value:
       raises('password_error', 400)

def validate_email(value):
    user = User.objects.filter(email=value)
    if user:
        raises('exist', 400, 'Email')
    return value