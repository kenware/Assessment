
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf.urls import handler404

from assessment.views.user import UserViewSet
from assessment.views.assessment_type import AssessmentTypeViewSet
from assessment.views.question import QuestionViewSet
from assessment.views.answer import AnswerViewSet
from assessment.views.assessment_score import UserScoreViewSet
from assessment.views.custom404 import custom404, http_mapper
from rest_framework_jwt.views import obtain_jwt_token
from assessment.views.assessment_events import AssessmentEventViewSet
from assessment.views.assessment_name import AssessmentNameViewSet

method = {
    'get': 'list',
    'post': 'create'
}

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'assessments/type', AssessmentTypeViewSet, base_name='assessmentTypes')
router.register(r'assessments', AssessmentNameViewSet, base_name='assessments')
router.register(r'questions', QuestionViewSet, base_name='questions')
router.register(r'answers', AnswerViewSet, base_name='answers')


handler404 = custom404

urlpatterns = [ 
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/v1/login/', obtain_jwt_token),
    path(r'api/v1/assessments/event/', AssessmentEventViewSet.as_view(method), name='survey'),
    path(r'api/v1/assessments/score/', UserScoreViewSet.as_view({'get':'list'}), name='score'),
    path(r'api/v1/', include(router.urls)),
    re_path(r'^.*$', custom404.as_view(http_mapper), name='error404'),   
] 
