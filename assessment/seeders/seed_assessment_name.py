

from assessment.models import AssessmentName


def seed_assessment_name():
    if not  AssessmentName.objects.filter(name='Practice assessment'):
       AssessmentName(name='Practice assessment').save()
       print('AssessmentName successfuly seeded >>>>>>')
