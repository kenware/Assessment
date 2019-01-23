# Liberaries
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

#Local modules
from assessment.models import Assessment
from assessment.serializers.question import EagerLoadQuestionSerializer

class AssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('id', 'title', 'max_time', 'total_mark', 'created_at')

class EagerLoadAssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    questions = EagerLoadQuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Assessment
        fields = ('id', 'title', 'max_time', 'total_mark', 'created_at', 'questions')
