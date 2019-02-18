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
class AssessmentTypeEndpointsTests(APITestCase):
    def test_get_all_assessment_with_children_succeeds(self):
        
        url = base_url + '/assessments/type/?include=children'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertIsInstance(response.data['results'][0]['questions'], list)
        self.assertIsInstance(response.data['results'][0]['questions'][0]['answers'], list)
    
    def test_include_children_with_wrong_value_fails(self):
        
        url = base_url + '/assessments/type/?include=childre'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_filter_colunm_with_wrong_data_type_fails(self):
        
        url = base_url + '/assessments/type/?totalMark="jj"'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
    
    def test_invalid_url_colunm_params_fails(self):
        
        url = base_url + '/assessments/type/?ark=700'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_order_by_with_wrong_params_fails(self):
        
        url = base_url + '/assessments/type/?order=ascId'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
    
    def test_order_by_without_asc_or_dec_before_colunm_name_fails(self):
        
        url = base_url + '/assessments/type/?orderBy=id'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_get_an_assessment_with_children_succeeds(self):
             
        question = TestFixtures.new_question_object()
        url = base_url + f'/assessments/type/{question.assessments_id}/?include=children'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['questions'], list)
        self.assertIsInstance(response.data['questions'][0]['answers'], list)
    
    def test_get_filtered_question_with_children_succeeds(self):
        
        url = base_url + '/questions/?include=children&startMark=301&endMark=309&questionText=today3'
        TestFixtures.question_list()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
 
        response = client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertIsInstance(response.data['results'][0]['answers'], list)
        self.assertEqual(response.data['results'][0]['questionText'], 'today3')
