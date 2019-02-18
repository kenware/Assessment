from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient
from datetime import datetime, timezone
import time

from assessment.models import Assessment, Answer, Score
client = APIClient()

#mock
from .mocks.userMock import valid_assessment

base_url = 'http://127.0.0.1:8000/api/v1'
class AssessmentEventEndpointsTests(APITestCase):
    def test_post_wrong_answer_to_question_does_not_increase_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        Score(user_id=user.id, assessments_id=question.assessments_id,\
        assessment_name_id=assessment.name_id,start_time=datetime.now(timezone.utc)).save()
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id)
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 0.00)

    def test_post_correct_answer_to_question_increase_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        Score(user_id=user.id, assessments_id=question.assessments_id,
        assessment_name_id=assessment.name_id, start_time=datetime.now(timezone.utc)).save()
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id, is_correct_choice=True)
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }
        response = client.post(url, data)
        print(response.data, 'kkkkkkkkkkkkkkkkkkk')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(response.data['score'], 0)

    def test_post_the_same_answer_of_a_question_does_not_change_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id, is_correct_choice=True)
        Score(correct_score=question.mark,user_id=user.id,
        assessment_name_id=assessment.name_id,assessments_id=question.assessments_id,\
        history={ f'{question.id}':[answer.id]},start_time=datetime.now(timezone.utc)).save()       
       
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }

        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], question.mark)
    
    def test_change_an_answer_to_a_question_change_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        wrong_answer = Answer.objects.create(choice_text='choice', questions_id=question.id)
        correct_answer = Answer.objects.create(choice_text='best choice', questions_id=question.id, is_correct_choice=True)
        Score(correct_score=0.00,user_id=user.id, assessment_name_id=assessment.name_id,assessments_id=question.assessments_id,\
        history={ f'{question.id}':[wrong_answer.id]},start_time=datetime.now(timezone.utc)).save()       
       
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': correct_answer.id
        }

        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(response.data['score'], 0.00)
    
    def test_post_wrong_answer_to_multi_choice_question_change_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_multi_choice_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        Score(user_id=user.id, assessments_id=question.assessments_id,\
        assessment_name_id=assessment.name_id,start_time=datetime.now(timezone.utc)).save()
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id, is_correct_choice=True)
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(response.data['score'], 0.00)

    def test_post_the_same_answer_of_a_question_change_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_multi_choice_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id, is_correct_choice=True)

        Score(correct_score=question.mark,user_id=user.id, assessment_name_id=assessment.name_id, assessments_id=question.assessments_id,\
        history={ f'{question.id}':[answer.id]},start_time=datetime.now(timezone.utc)).save()       
       
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }

        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(response.data['score'], question.mark)

    def test_post_the_different_answer_of_a_multi_choice_question_increases_score(self):      

        url = base_url + '/assessments/event/'
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_multi_choice_question_object()
        answer = Answer.objects.create(choice_text='choice', questions_id=question.id, is_correct_choice=True)

        assessment = Assessment.objects.get(pk=question.assessments_id)
        Score(correct_score=question.mark,user_id=user.id,\
        assessment_name_id=assessment.name_id,assessments_id=question.assessments_id,\
        history={ f'{question.id}':[14]},start_time=datetime.now(timezone.utc)).save()       
       
        data = {
            'assessmentId': question.assessments_id,
            'questionId': question.id,
            'answerId': answer.id
        }

        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(response.data['score'], question.mark)
