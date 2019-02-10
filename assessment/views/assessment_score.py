

# Liberaries
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from functools import partial

# Local modules.
from assessment.models import Score, User, Assessment
from assessment.serializers.score import ScoreSerializer
from assessment.helpers.permission import StaffAuthenticatedPermission, AllowedUserPermission
from assessment.helpers.query_parser import QueryParser
from assessment.middlewares.validators.score_history_validator import get_paginated_history
from assessment.middlewares.validators.field_validators import get_object_or_404, get_or_404
from assessment.middlewares.validators.errors import raises_error

class UserScoreViewSet(viewsets.ModelViewSet): 
    permission_classes = (IsAuthenticated, partial(AllowedUserPermission,['GET'], StaffAuthenticatedPermission),)
   
    def get_score_user_id_or_assessment_id(self, query, request):
        assessment_id = query.get('assessmentId')
        user_id = query.get('userId')
        page = query.get('page')
        page_number = page if page and int(page) > 0 else 1

        if user_id and assessment_id:
            get_or_404(User, user_id) 
            get_or_404(Assessment, assessment_id)
            scores = Score.objects.filter(user_id=user_id, assessments_id=assessment_id)
            
            prev, next, score = get_paginated_history(scores, page_number, assessment_id, user_id, request)

            data = ScoreSerializer(score).data
            data['attempt'] = page_number
            data['totalAttempt'] = len(scores)

            return Response({'result': [data], 'previous': prev, 'next': next}) 
        else:
            raises_error('history_error', 400)

    def get_user_score_with_history(self, include, query, request):
        raises_error('include_error', 400, include) if include != 'history' else None
       
        score_id = query.get('id')

        if score_id:
            score = get_object_or_404(Score, score_id)
            return Response(ScoreSerializer(score).data)
        else:

            return self.get_score_user_id_or_assessment_id(query, request)
 
    def list(self, request):
        query = request.query_params
        
        include = query.get('include')
        if include:
            return self.get_user_score_with_history(include, query, request)
        else:
            user_scores = QueryParser.parse_all(self, Score, query, ScoreSerializer, None)
            return user_scores
