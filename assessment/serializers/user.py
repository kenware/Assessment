from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from assessment.middlewares.validators.errors import raises
from assessment.middlewares.validators.field_validators import validate_password

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
    
    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raises('exist', 400, 'Email')
        return value

    def validate_password(self, value):
        validate_password(value)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    