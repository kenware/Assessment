from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient

from assessment.models import Question
client = APIClient()

#mock
from .mocks.userMock import valid_question

base_url = 'http://127.0.0.1:8000/api/v1'
class QuestionEndpointsTests(APITestCase):
    def test_create_new_question_succeeds(self):      

        url = base_url + '/questions/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        assessment = TestFixtures.new_assessment_object()
        print(assessment, 'nnnnnnnnnnnnnnnnnnnn')

        valid_question['assessmentId'] = assessment.id
        response = client.post(url, valid_question)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['question_text'], valid_question['questionText'])
        self.assertEqual(response.data['mark'], valid_question['mark'])
        self.assertEqual(response.data['number'], valid_question['number'])

    def test_create_question_without_token_fails(self):
        
        url = base_url + '/questions/'
        response = self.client.post(url, valid_question)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_question_succeeds(self):
        
        url = base_url + '/questions/'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 5)
    
    def test_update_question_succeeds(self):
        client = APIClient()
        new_question =  TestFixtures.new_question_object()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        valid_question['assessmentId'] = new_question.assessments_id
        url = base_url + f'/questions/{new_question.id}/'
        response = client.patch(url, valid_question)
        self.assertEqual(response.data['question_text'], valid_question['questionText'])
        self.assertEqual(response.data['mark'], valid_question['mark'])


    def test_delete_question_succeeds(self):
        client = APIClient()
        new_question =  TestFixtures.new_question_object()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        url = base_url + f'/questions/{new_question.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    


              