# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Question, Answer
from assessment.serializers.answer import AnswerSerializer
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.helpers.query_parser import QueryParser
from assessment.middlewares.validators.answer_validator import (
    is_answer_set_validator, is_same_choice_validator, validate_correct_answer)
from assessment.helpers.get_all_endpoints import get_paginated_and_query_filtered_data


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all() #pylint: disable=E1101

    list = get_paginated_and_query_filtered_data( Answer, AnswerSerializer, None)

    def create(self, request):
 
        answer_data = AnswerSerializer(data=request.data)
        answer_data.is_valid(raise_exception=True)
        question = Question.objects.get(pk=request.data.get('question_id'))#pylint: disable=E1101     
    
        if request.data.get('is_correct_choice'):     
            is_answer_set_validator(question)
        
        if not question.multi_choice:
            is_same_choice_validator(question, request.data)

        answer = answer_data.save()
        answer = AnswerSerializer(answer).data
        return Response(answer, 201)

    def partial_update(self, request, pk=None):
        answer_data = AnswerSerializer(data=request.data, partial=True)
        answer_data.is_valid(raise_exception=True)
        answer = Answer.objects.get(pk=pk)#pylint: disable=E1101
        question = Question.objects.get(pk=answer.questions_id)#pylint: disable=E1101
        if not question.multi_choice:
            correct_answer = Answer.objects.filter(questions_id=question.id, is_correct_choice=True)#pylint: disable=E1101
            validate_correct_answer(correct_answer, request, answer)
        answer = answer_data.update(answer, request.data) 
        answer = AnswerSerializer(answer).data
        return Response({
            'message': 'Answer successfully updated',
            'answer': answer})
