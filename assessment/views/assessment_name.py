# Liberaries
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from functools import partial

# Local modules.
from assessment.models import AssessmentName
from assessment.helpers.retrieve_endpoint import retrieve_filtered_data
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.helpers.query_parser import QueryParser
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data
from assessment.serializers.assessment_name import AssessmentNameSerializer, EagerLoadAssessmentNameSerializer

class AssessmentNameViewSet(viewsets.ModelViewSet):
    """
    Assessment name viewsets
    """
    serializer_class = AssessmentNameSerializer
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    queryset = AssessmentName.objects.all() #pylint: disable=E1101
    
    list = get_paginated_and_query_filtered_data(AssessmentName, AssessmentNameSerializer, EagerLoadAssessmentNameSerializer)

    retrieve = retrieve_filtered_data(AssessmentName, AssessmentNameSerializer, EagerLoadAssessmentNameSerializer)
