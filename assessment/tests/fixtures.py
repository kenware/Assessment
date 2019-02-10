from .mocks.userMock import valid_user, valid_assessment, valid_question
from django.contrib.auth.models import User
from assessment.models import Assessment, Question, Answer, Score
from assessment.helpers.token_generator import generate_token
from datetime import datetime, timezone

class TestFixtures():
    def new_user():
        user = User.objects.create(email=valid_user['email'], username=valid_user['username'], password=valid_user['password'])
        return user

    def auth_token():
        user = User(email='kenware@gmail.com', username='kenware2', is_staff=True)
        user.save()
        token = generate_token(user)
        return token
    
    def auth_user_token():
        user = User.objects.create(email='kenware@gmail.com', username='kenware2', is_staff=True)
        token = generate_token(user)
        return token, user

    def list_of_user():
        for n in range(5):
            user = User(email=valid_user['email'] + str(n), username=valid_user['username'] + str(n))
            user.save()
    
    def new_assessment():
        new_assessment = Assessment(title=valid_assessment['title'], max_time=valid_assessment['maxTime'],total_mark=100)
        return new_assessment
    
    def new_assessment_object():
        new_assessment =  TestFixtures.new_assessment()
        TestFixtures.new_assessment().save()
        assessment = Assessment.objects.get(title=new_assessment.title) #pylint: disable=E1101
        return assessment

    def question_list():
        new_assessment =  TestFixtures.new_assessment_object()
        for n in range(5):
            question = Question(assessments_id=new_assessment.id, question_text='today' + str(n),mark=300 + n)
            question.save()

    def new_question_object():
        new_assessment =  TestFixtures.new_assessment_object()
        return Question.objects.create(assessments=new_assessment, question_text='what is todays date',mark=300)

    def new_multi_choice_question_object():
        new_assessment =  TestFixtures.new_assessment_object()
        return Question.objects.create(assessments=new_assessment, question_text='what is todays date',mark=300, multi_choice=True)
        
    def correct_choice():
        question = TestFixtures.new_multi_choice_question_object()
        return Answer.objects.create(choice_text='correct choice', is_correct_choice=True, questions_id=question.id)#pylint: disable=E1101

    def choice():
        question = TestFixtures.new_question_object()
        return Answer.objects.create(choice_text='correct choice', questions_id=question.id)#pylint: disable=E1101

    def choice_list():
        question = TestFixtures.new_question_object()
        for n in range(5):
            answer = Answer(questions_id=question.id, choice_text='today' + str(n))
            answer.save()
        return question.id

    def user_score():
        token, user = TestFixtures.auth_user_token()
        question = TestFixtures.new_question_object()
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id)
        history = {question.id : [answer.id]}
        score = Score.objects.create(user_id=user.id, assessments_id=question.assessments.id,start_time=datetime.now(timezone.utc), history=history, status='finished')
        return token, user, question, answer, score
        

