# Liberaries
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Assessment
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.assessment_type import AssessmentTypeSerializer


class AssessmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = AssessmentTypeSerializer
    queryset = Assessment.objects.all() #pylint: disable=E1101
