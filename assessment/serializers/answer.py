
# Liberaries
from rest_framework import serializers

# Local modules.
from assessment.models import Question, Answer
from assessment.middlewares.validators.field_validators import get_or_404



class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    question_id = serializers.IntegerField(source='questions_id')
    class Meta:
        model = Answer
        fields = ('id', 'choice_text', 'question_id', 'image_url','created_at')

    def validate_question_id(self, value):      
        get_or_404(Question, value)
        return value
