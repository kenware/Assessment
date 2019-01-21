from assessment.models import Answer
from assessment.middlewares.validators.errors import raises_error


def is_answer_set_validator(question):
    if not question.multi_choice:
        is_correct_answer_set = Answer.objects.\
        filter(questions_id=question.id,is_correct_choice=True)
        
        if is_correct_answer_set:
           raises_error('answer_set', 400, question.id)

def is_same_choice_validator(question, request):
    same_choice_text = Answer.objects.filter(questions_id=question.id, choice_text=request['choice_text'])
    if same_choice_text:
       raises_error('choice_exist', 400, question.id)

def validate_correct_answer(correct_answer, request, answer):
    if correct_answer and (correct_answer[0].id != answer.id)\
    and request.data.get('is_correct_choice'):
        correct_answer[0].is_correct_choice = False
        correct_answer[0].save()
