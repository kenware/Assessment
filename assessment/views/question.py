# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Question
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.question import QuestionSerializer, EagerLoadQuestionSerializer
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all() #pylint: disable=E1101

    list = get_paginated_and_query_filtered_data(Question, QuestionSerializer, EagerLoadQuestionSerializer)
