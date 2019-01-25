
from datetime import datetime, timezone, time
from rest_framework.response import Response
from decimal import Decimal

from assessment.models import Score, Answer
from assessment.middlewares.validators.errors import raises_error


def validate_assessment_taken(score_object, assessment, user):
    score_object = score_object.last()
    if assessment.multi_times and score_object.status == 'finished':
        score_object = Score.objects.create(user=user, assessments=assessment, start_time=datetime.now(timezone.utc))
        return score_object  
    if score_object.status == 'finished':
        raises_error('assessment_end', 400)
    return score_object

def validate_assessment_time(score_object, assessment):
    
    mapper = {
            True: 'multi_times_assessment',
            False: 'single_time_assessment'
    }
    
    start_time = score_object.start_time 
    current_time = datetime.now(timezone.utc) 
    max_time = assessment.max_time
    
    time_different = current_time - start_time
    hour, minutes= time_different.seconds//3600, (time_different.seconds//60)%60

    time_different = time(hour, minutes)
    if time_different >= max_time:
       score_object.status='finished'
       score_object.save() 
       raises_error(mapper.get(assessment.multi_times), 400)

def get_mark_from_question(question):
    if question.multi_choice:
        correct_choices_count = Answer.objects.filter(questions_id=question.id, is_correct_choice=True).count()
        mark = question.mark/correct_choices_count
        return mark
    return question.mark

def get_actual_mark_based_on_choice(question, answer_id):
    mark = get_mark_from_question(question)
    is_correct_choice = Answer.objects.filter(id=answer_id, questions_id=question.id, is_correct_choice=True).first()
    mark = mark if is_correct_choice else -(Decimal(0.25) * mark) if question.multi_choice else 0
    return mark
          

def update_multi_choice_history(*args):
     history, question, answer_id, mark, user_score = args

     answer_id_list = history[str(question.id)]
     if answer_id in answer_id_list:
        mark = get_actual_mark_based_on_choice(question, answer_id)
        answer_id_list.remove(answer_id)
        history[str(question.id)] = answer_id_list
        user_score.correct_score -= round(mark, 2)
        user_score.save()
        return history, user_score
     history[str(question.id)].append(answer_id)
     user_score.correct_score += mark
     user_score.save()
     return history, user_score

def validate_history(*args):
    history, question, answer_id, mark, user_score = args
    
    if question.multi_choice:
        history, user_score = update_multi_choice_history(history, question, answer_id, mark, user_score)
        return history, user_score

    previous_answer_id = history[str(question.id)][0]
    previous_mark = get_actual_mark_based_on_choice(question, previous_answer_id)

    user_score.correct_score -= round(previous_mark, 2)
    user_score.save()
    user_score.correct_score += mark
    user_score.save()
    history[str(question.id)] = [answer_id]
    return history, user_score

def validate_change_question_answer(history, question, answer_id, user_score):

    mark = get_actual_mark_based_on_choice(question, answer_id)
    mark = round(mark,2)

    question_history = history.get(str(question.id))    
    if question_history:
        history, user_score = validate_history(history, question, answer_id, mark, user_score)

    else:
        current_history = { str(question.id): [answer_id]}
        history.update(current_history)
        user_score.correct_score += mark
        user_score.save()
    return history, user_score