# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial
from django.shortcuts import get_object_or_404

# Local modules.
from assessment.models import Assessment
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.assessment_type import AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer
from assessment.helpers.query_parser import QueryParser
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data


class AssessmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = AssessmentTypeSerializer
    queryset = Assessment.objects.all() #pylint: disable=E1101
    
    list = get_paginated_and_query_filtered_data(Assessment, AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer)

    def retrieve(self, request, pk=None):
        url_query = request.query_params
        queryset = get_object_or_404(Assessment, pk=pk)
        assessment_data = QueryParser.include_children(AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer, url_query, queryset, False) 
        return Response(assessment_data)
