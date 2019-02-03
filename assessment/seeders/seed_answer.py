from assessment.models import Question, Answer

def seed_answer():
    
    question = Question.objects.all()
    question1 = question[0]
    question2 = question[1]
    question3 = question[2]
    question4 = question[3]

    answer_data = [
        Answer(choice_text='went', is_correct_choice=True,questions_id=question1.id),
        Answer(choice_text='gone', is_correct_choice=True,questions_id=question1.id),
        Answer(choice_text='come', questions_id=question1.id),
        Answer(choice_text='1960', is_correct_choice=True,questions_id=question2.id),
        Answer(choice_text='1930', questions_id=question2.id),
        Answer(choice_text='one year old', is_correct_choice=True,questions_id=question3.id),
        Answer(choice_text='A year old', is_correct_choice=True,questions_id=question3.id),
        Answer(choice_text='Three years old', questions_id=question3.id),
        Answer(choice_text='24', is_correct_choice=True,questions_id=question4.id),
        Answer(choice_text='48', questions_id=question4.id),
        Answer(choice_text='sun', is_correct_choice=True,questions_id=question4.id),
        Answer(choice_text='moon', questions_id=question4.id),
    ]
    for answer in answer_data:
        answer.save()
        print('answer successfuly seeded >>>>>>')
