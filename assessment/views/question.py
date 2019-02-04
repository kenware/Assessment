# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Question, Assessment
from assessment.middlewares.validators.field_validators import get_object_or_404
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
    
    def destroy(self, request, pk=None):
        question = get_object_or_404(Question, pk)
        assessment_id = question.assessments_id
        assessment = get_object_or_404(Assessment, assessment_id)
        assessment.total_mark -= question.mark
        assessment.save()
        question.delete()
        return Response(None, 204)
