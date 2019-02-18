

from assessment.models import Assessment, AssessmentName


def seed_assessment():
    name = AssessmentName.objects.all()[0]
    
    assessment_data = [
            Assessment(type='Verbal reasoning', multi_times=True, max_time='00:23:00', name=name),
            Assessment(type='Quantitative reasoning',  max_time='00:10:00', name=name),
            Assessment(type='Antonymes', multi_times=True, max_time='00:1:00', name=name),
            Assessment(type='Sinonymes', multi_times=True, max_time='00:1:00', name=name)
       ]

    for assessment in assessment_data:
        if not Assessment.objects.filter(type=assessment.type, name_id=name.id):
           assessment.save()
           print('Assessment type successfuly seeded >>>>>>')
