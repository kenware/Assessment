# Liberaries
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

#Local modules
from assessment.models import AssessmentName
from assessment.serializers.assessment_type import EagerLoadAssessmentTypeSerializer
from assessment.middlewares.validators.field_validators import get_or_404

class AssessmentNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssessmentName
        fields = ('id', 'name', 'created_at')

class EagerLoadAssessmentNameSerializer(serializers.HyperlinkedModelSerializer):
    assessments = EagerLoadAssessmentTypeSerializer(read_only=True, many=True)
    class Meta:
        model = AssessmentName
        fields = ('id', 'name', 'created_at','assessments')
    