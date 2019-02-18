# Liberaries
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

#Local modules
from assessment.models import Assessment, AssessmentName
from assessment.serializers.question import EagerLoadQuestionSerializer
from assessment.middlewares.validators.field_validators import get_or_404
from assessment.middlewares.validators.errors import raises_error

class AssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    name_id = serializers.IntegerField()
    class Meta:
        model = Assessment
        fields = ('id', 'type', 'max_time', 'total_mark', 'created_at', 'name_id')

    def validate_name_id(self, value):      
        get_or_404(AssessmentName, value)
        return value
    
    def create(self, validated_data):

        name_id = validated_data.get('name_id')
        type = validated_data.get('type')
        if Assessment.objects.filter(type=type, name_id=name_id):
            raises_error('type_error', 400)
 
        return Assessment.objects.create(**validated_data) 


class EagerLoadAssessmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    questions = EagerLoadQuestionSerializer(read_only=True, many=True)
    name_id = serializers.IntegerField()
    class Meta:
        model = Assessment
        fields = ('id', 'type', 'max_time', 'total_mark', 'created_at', 'questions', 'name_id')
    
    def validate_name_id(self, value):      
        get_or_404(AssessmentName, value)
        return value

