
# Liberaries
from rest_framework import serializers

# Local modules.
from assessment.models import Score, Question, Answer
from assessment.middlewares.validators.field_validators import get_object_or_404
from assessment.serializers.user import UserSerializer
from assessment.serializers.assessment_type import AssessmentTypeSerializer
from assessment.serializers.question import QuestionSerializer
from assessment.serializers.answer import AnswerSerializer


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    assessments = AssessmentTypeSerializer(read_only=True) 
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Score
        fields = ('id', 'start_time', 'end_time', 'status', 'user','assessments', 'score', 'history') 
 
    def get_score(self, obj):
        return f'{(obj.correct_score/(obj.assessments.total_mark))*100}%'
     
    def get_history(self, obj):
        history = obj.history
        history_list = []
        print(history)
        for key, values in history.items():
            key = int(key)
            question = get_object_or_404(Question, key)
            question = QuestionSerializer(question).data
            choice = []
            for id in values:
                answer = get_object_or_404(Answer, id)
                answer = AnswerSerializer(answer).data
                choice.append(answer)
            history_object = {
                'question': question,
                'choice': choice
            }
            history_list.append(history_object)

        return history_list 
