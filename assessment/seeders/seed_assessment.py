

from assessment.models import Assessment


def seed_assessment():
    
    assessment_data = [
            Assessment(title='survey', multi_times=True, max_time='00:23:00'),
            Assessment(title='new assessment',  max_time='00:10:00'),
            Assessment(title='andela survey', multi_times=True, max_time='00:1:00')
       ]

    for assessment in assessment_data:
        assessment.save()
        print('Assessment type successfuly seeded >>>>>>')
