from .mocks.userMock import valid_user, valid_assessment, valid_question
from django.contrib.auth.models import User
from assessment.models import Assessment, Question
from assessment.helpers.token_generator import generate_token

class TestFixtures():
    def new_user():
        user = User(email=valid_user['email'], username=valid_user['username'])
        return user

    def auth_token():
        user = User(email='kenware@gmail.com', username='kenware2', is_staff=True)
        user.save()
        token = generate_token(user)
        return token

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
        question = Question(assessments=new_assessment, question_text='what is todays date',mark=300)
        question.save()
        return Question.objects.get(question_text=question.question_text) #pylint: disable=E1101