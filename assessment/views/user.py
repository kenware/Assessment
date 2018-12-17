from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from assessment.serializers.user import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
class MyviewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self, request):

        print(request.user.username, 'jjjjjjjjjjjjjjjjjjjjjj')
        return Response({"new":"newe"})