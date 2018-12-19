from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from assessment.middlewares.validators.errors import raises
from assessment.middlewares.validators.field_validators import validate_password, validate_email

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',)

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)
    
    def create(self, validated_data):

        email = validated_data.get('email')
        validate_email(email)
        user = User.objects.create(**validated_data)
        return user

    