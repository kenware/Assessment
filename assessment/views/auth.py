from django.shortcuts import render
from rest_framework.request import Request
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class AuthViewSet(viewsets.ViewSet):
    """
    API endpoint that authenticate user.
    """
  
    def create(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)