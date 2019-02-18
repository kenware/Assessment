
from assessment.models import Question, Assessment
from assessment.middlewares.validators.field_validators import get_object_or_404

def seed_question():
    
    assessment = Assessment.objects.all()
    assessment1 = assessment[0]
    assessment2 = assessment[1]
    assessment3= assessment[2]

    question_data = [
        Question(question_text='What is the past tense of go?', assessments_id=assessment1.id,mark=2,multi_choice=True),
        Question(question_text='when did Nigeria gain independence', assessments_id=assessment1.id,mark=2),
        Question(question_text='A boy is two years old. How old is he last year?', assessments_id=assessment2.id,mark=2,multi_choice=True),
        Question(question_text='How many hours make one day?', assessments_id=assessment2.id,mark=2),
        Question(question_text='The earth rotate round the following', assessments_id=assessment3.id,mark=2,multi_choice=True),
        Question(question_text='How many hours make one day?', assessments_id=assessment3.id,mark=2),
    ]
    for question in question_data:
        assessment = get_object_or_404(Assessment, question.assessments_id)
        if not Question.objects.filter(question_text=question.question_text):
            assessment.total_mark += question.mark
            assessment.save()
            question.save()
            print('questions successfuly seeded >>>>>>')
