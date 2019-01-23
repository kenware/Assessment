# Liberaries
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.shortcuts import get_object_or_404

# local modules
from assessment.models import Question
from assessment.middlewares.validators.field_validators import get_or_404
from assessment.models import Assessment, Question
from assessment.serializers.answer import AnswerSerializer


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    assessment_id = serializers.IntegerField(source='assessments_id')
    class Meta:
        model = Question
        fields = ('id', 'mark', 'question_text', 'number','correct_choices', 'multi_choice', 'assessment_id', 'image_url','created_at')

    def validate_assessment_id(self, value):      
        get_or_404(Assessment, value)
        return value

class EagerLoadQuestionSerializer(serializers.HyperlinkedModelSerializer):
    assessment_id = serializers.IntegerField(source='assessments_id')
    answers = AnswerSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ('id', 'mark', 'question_text', 'number','correct_choices', 'multi_choice', 'assessment_id', 'image_url','created_at','answers')

    def validate_assessment_id(self, value):      
        get_or_404(Assessment, value)
        return value
