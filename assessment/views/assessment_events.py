# Liberaries
from datetime import datetime, timezone
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from functools import partial
from django.shortcuts import get_object_or_404


# Local modules.
from assessment.models import Assessment, Question, Score, Answer
#helpers
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.helpers.query_parser import QueryParser
#serializers
from assessment.serializers.assessment_type import AssessmentTypeSerializer, EagerLoadAssessmentTypeSerializer
from assessment.serializers.question import QuestionSerializer, EagerLoadQuestionSerializer
#middlewares
from assessment.middlewares.validators.validate_assessment_events import (
    validate_assessment_taken,
    get_mark_from_question,
    validate_change_question_answer,
    get_actual_mark_based_on_choice,
    validate_assessment_time)
from assessment.middlewares.validators.field_validators import get_object_or_404

class AssessmentEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
    
    def list(self, request):
        query = request.query_params 
        assessment_id = query.get('assessmentId')
        assessment = get_object_or_404(Assessment, assessment_id)

        user = request.user
        user_score = Score.objects.filter(user_id=user.id, assessments_id=assessment_id)
        if user_score:
            user_score = validate_assessment_taken(user_score, assessment, user)    
        else:
            user_score = Score.objects.create(user=user, assessments=assessment, start_time=datetime.now(timezone.utc))
    
        validate_assessment_time(user_score, assessment)
        assessment_data = AssessmentTypeSerializer(assessment).data       
        question_data = QueryParser.parse_all(self, Question, query, QuestionSerializer, EagerLoadQuestionSerializer)

        assessment_data['questions'] = question_data.data 
        assessment_data['start_time'] = user_score.start_time
        assessment_data['max_time'] = assessment.max_time

        return Response(assessment_data) 
    
    def create(self, request):
        data = request.data
        user = request.user

        assessment_id, question_id, answer_id = data.get('assessment_id'), data.get('question_id'), data.get('answer_id')
        assessment = get_object_or_404(Assessment, assessment_id)
        question = get_object_or_404(Question, question_id)
        answer = get_object_or_404(Answer, answer_id)
        
        user_score = Score.objects.filter(user_id=user.id, assessments_id=assessment_id).last()
        validate_assessment_time(user_score, assessment)

        history = user_score.history
        new_history, user_score = validate_change_question_answer(history, question, answer_id, user_score)
        user_score.history = new_history
        user_score.save()
        return Response({'score': user_score.correct_score, 'user': user.username, 'history':user_score.history}, 201)
