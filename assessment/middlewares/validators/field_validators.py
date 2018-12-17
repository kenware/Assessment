
from rest_framework import serializers
from .errors import raises

def validate_password(value):  
   if len(value)<4 or not value:
       raises('password_error', 400)