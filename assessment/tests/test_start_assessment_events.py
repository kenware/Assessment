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

    def test_start_assessments_succeeds(self):
        question = TestFixtures.new_question_object()

        Answer.objects.create(choice_text='choice', questions_id=question.id)
        url = f'{base_url}/assessments/event/?assessmentId={question.assessments_id}&include=children'
        
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['questions'], dict)
        self.assertIsInstance(response.data['questions']['results'], list)
        self.assertIsInstance(response.data['questions']['results'][0]['answers'], list)
       
    def test_get_assessment_in_progress_succeed(self):
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments.id)
        Score(user_id=user.id, assessments_id=question.assessments_id,\
        start_time=datetime.now(timezone.utc),assessment_name_id=assessment.name_id).save()
        
        Answer.objects.create(choice_text='choice', questions_id=question.id)
        url = f'{base_url}/assessments/event/?assessmentId={question.assessments_id}&include=children'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['questions'], dict)
        self.assertIsInstance(response.data['questions']['results'], list)
        self.assertIsInstance(response.data['questions']['results'][0]['answers'], list)

    def test_get_multitimes_assessment_with_status_finished_succeed(self):
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        question = TestFixtures.new_multi_choice_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        assessment.multi_times = True
        assessment.save()
        Score(user_id=user.id, assessments_id=question.assessments_id,\
        start_time=datetime.now(timezone.utc), status='finished', assessment_name_id=assessment.name_id).save()
        
        Answer.objects.create(choice_text='choice', questions_id=question.id)
        url = f'{base_url}/assessments/event/?assessmentId={question.assessments_id}&include=children'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['questions'], dict)
        self.assertIsInstance(response.data['questions']['results'], list)
        self.assertIsInstance(response.data['questions']['results'][0]['answers'], list)
    
    def test_get_non_multitimes_assessment_with_status_finished_fails(self):
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments.id)
        Score(user_id=user.id, assessments_id=question.assessments_id,start_time=datetime.now(timezone.utc),\
        status='finished', assessment_name_id=assessment.name_id).save()
        
        Answer.objects.create(choice_text='choice', questions_id=question.id)
        url = f'{base_url}/assessments/event/?assessmentId={question.assessments_id}&include=children'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
    
    def test_get_assessment_with_time_used_up_fails(self):
        token, user = TestFixtures.auth_user_token()
        token = 'Bearer ' + token

        question = TestFixtures.new_question_object()
        assessment = Assessment.objects.get(pk=question.assessments_id)
        assessment.max_time = '00:00:00'
        assessment.save()

        Score(user_id=user.id, assessments_id=question.assessments_id,\
        start_time=datetime.now(timezone.utc), assessment_name_id=assessment.name_id).save()
        Answer.objects.create(choice_text='choice', questions_id=question.id)
        url = f'{base_url}/assessments/event/?assessmentId={question.assessments_id}&include=children'
        
        client.credentials(HTTP_AUTHORIZATION=token)
        time.sleep(1)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
    