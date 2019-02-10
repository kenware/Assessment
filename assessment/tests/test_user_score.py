from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient
from datetime import datetime, timezone
import time

from assessment.models import Assessment, Answer, Score
from assessment.middlewares.validators.messages import error_messages
client = APIClient()

#mock
from .mocks.userMock import valid_assessment

base_url = 'http://127.0.0.1:8000/api/v1'
class UseScoreEndpointsTests(APITestCase):

  
    def test_get_all_user_score(self):
        token = TestFixtures.auth_token()
        token = 'Bearer ' + token

        url = f'{base_url}/assessments/score/'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
    
    def test_get_a_user_score_succeed(self):
        token, user, question, answer, score = TestFixtures.user_score()
        token = 'Bearer ' + token

        url = f'{base_url}/assessments/score/?id={score.id}&include=history'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['user'], dict)
        self.assertIsInstance(response.data['assessments'], dict)

    def test_get_a_user_score_with_wrong_include_fails(self):
        token, user, question, answer, score = TestFixtures.user_score()
        token = 'Bearer ' + token

        url = f'{base_url}/assessments/score/?id={score.id}&include=histor'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], error_messages['include_error'].format('histor'))
    
    def test_get_a_user_score_with_assessment_id_and_user_id_succeed(self):
        token, user, question, answer, score = TestFixtures.user_score()
        token = 'Bearer ' + token

        url = f'{base_url}/assessments/score/?assessmentId={question.assessments_id}&userId={user.id}&include=history'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['next'], 'null')
        self.assertEqual(response.data['previous'], 'null')
    
    def test_get_a_user_score_with_history_and_without_user_id_fails(self):
        token, user, question, answer, score = TestFixtures.user_score()
        token = 'Bearer ' + token

        url = f'{base_url}/assessments/score/?assessmentId={question.assessments_id}&include=history'
        
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], error_messages['history_error'])
    