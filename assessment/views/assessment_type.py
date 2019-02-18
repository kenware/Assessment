# Liberaries
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Assessment
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.assessment_type import AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer
from assessment.helpers.query_parser import QueryParser
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data
from assessment.helpers.retrieve_endpoint import retrieve_filtered_data

class AssessmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = AssessmentTypeSerializer
    queryset = Assessment.objects.all() #pylint: disable=E1101
    
    list = get_paginated_and_query_filtered_data(Assessment, AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer)

    retrieve = retrieve_filtered_data(Assessment, AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer)
