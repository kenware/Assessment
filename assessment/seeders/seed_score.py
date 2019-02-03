
from django.contrib.auth.models import User
from datetime import datetime, timezone

from assessment.models import Score, Question, Answer
from assessment.middlewares.validators.validate_assessment_events import get_mark_from_question

def get_score_instance(user_id, assessment_id, *args):
    history = {}
    total_mark = 0

    for question in args:
       correct_answer = Answer.objects.filter(questions_id=question.id, is_correct_choice=True).last()
       mark = get_mark_from_question(question)
       total_mark += mark
       history.update({str(question.id): [correct_answer.id]})
    
    return Score(user_id=user_id, assessments_id=assessment_id,\
        start_time=datetime.now(timezone.utc), history=history,correct_score=total_mark)



def seed_score():
    users = User.objects.all()
    questions = Question.objects.all()
    question1 = questions[0]
    question2 = questions[1]
    question3 = questions[2]
    question4 = questions[3]

    score_data = [
            get_score_instance(users[0].id, question2.assessments_id, question1, question2),
            get_score_instance(users[1].id, question4.assessments_id, question3, question4)          
       ]

    for score in score_data:
        score.save()
        print('Score successfuly seeded >>>>>>')
