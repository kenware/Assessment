from assessment.models import Assessment
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from assessment.middlewares.validators.errors import raises
from assessment.middlewares.validators.field_validators import validate_password, validate_email
from assessment.serializers.question import QuestionSerializer, EagerLoadQuestionSerializer
class AssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('id', 'title', 'max_time', 'total_mark', 'created_at')

class EagerLoadAssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    questions = EagerLoadQuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Assessment
        fields = ('id', 'title', 'max_time', 'total_mark', 'created_at', 'questions')
