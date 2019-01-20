# Liberaries
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Question, Assessment
from assessment.serializers.assessment_type import AssessmentTypeSerializer
from assessment.serializers.question import QuestionSerializer
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.serializers.question import QuestionSerializer, EagerLoadQuestionSerializer
from assessment.helpers.query_parser import QueryParser


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all() #pylint: disable=E1101

    def list(self, request):
        url_query = request.query_params
        question_data = QueryParser.parse_all(Question, url_query, QuestionSerializer, EagerLoadQuestionSerializer)
        return Response(question_data)


