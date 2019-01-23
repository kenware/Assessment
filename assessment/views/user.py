# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from functools import partial

# Local modules.
from django.contrib.auth.models import User
from assessment.helpers.token_generator import generate_token
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.user import UserSerializer
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (partial(AllowedUserPermission,['POST'], StaffAuthenticatedPermission),)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = generate_token(user)
        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data['token'] = token
        return Response(user_data)

    list = get_paginated_and_query_filtered_data(User, UserSerializer, None)
