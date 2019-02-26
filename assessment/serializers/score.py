
# Liberaries
from rest_framework import serializers

# Local modules.
from assessment.models import Score, Question, Answer
from assessment.middlewares.validators.field_validators import get_object_or_404
from assessment.serializers.user import UserSerializer
from assessment.serializers.assessment_type import AssessmentTypeSerializer
from assessment.serializers.question import QuestionSerializer
from assessment.serializers.answer import AnswerSerializer
from assessment.serializers.assessment_name import AssessmentNameSerializer


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.SerializerMethodField()
    assessments = AssessmentTypeSerializer(read_only=True) 
    user = UserSerializer(read_only=True)
    assessment_name = AssessmentNameSerializer(read_only=True)
    
    class Meta:
        model = Score
        fields = ('id', 'start_time', 'end_time', 'status', 'user','assessments', 'score', 'assessment_name', 'history')
 
    def get_score(self, obj):
        score = float(obj.correct_score) if float(obj.correct_score) > 0 else 0.1
        total_mark = float(obj.assessments.total_mark)
        total_mark = total_mark if total_mark > 0 else 0.1
        return f'{(score/(total_mark))*100}%'
    
class ScoreHistorySerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    assessments = AssessmentTypeSerializer(read_only=True) 
    user = UserSerializer(read_only=True)
    assessment_name = AssessmentNameSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ('id', 'start_time', 'end_time', 'status', 'user','assessments', 'score', 'history', 'assessment_name') 
 
    def get_score(self, obj):
        score = float(obj.correct_score) if float(obj.correct_score) > 0 else 0.1
        total_mark = float(obj.assessments.total_mark)
        total_mark = total_mark if total_mark > 0 else 0.1
        return f'{(score/(total_mark))*100}%'
     
    def get_history(self, obj):
        history = obj.history
        history_list = []
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
