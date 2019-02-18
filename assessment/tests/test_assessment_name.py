from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient

from assessment.models import Assessment
client = APIClient()
valid_assessment_name = {'name': 'andelay assessment'}

base_url = 'http://127.0.0.1:8000/api/v1'
class AssessmentNameEndpointsTests(APITestCase):
    def test_create_new_assessment_name_succeeds(self):      
       
        url = base_url + '/assessments/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        
        response = client.post(url, valid_assessment_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], valid_assessment_name['name'])

    def test_create_assessment_with_already_existing_name_fails(self):
        
        url = base_url + '/assessments/'
        assessment_name = TestFixtures.new_assessment_name()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        valid_assessment_name['name'] = assessment_name.name

        response = client.post(url, valid_assessment_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_assessment_name_without_token_fails(self):
        
        url = base_url + '/assessments/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_assessments_succeeds(self):
        
        url = base_url + '/assessments/'
        TestFixtures.new_assessment_name()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertIsInstance(response.data, dict)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_update_assessment_succeeds(self):
        client = APIClient()
        new_assessment_name =  TestFixtures.new_assessment_name()
   
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/{new_assessment_name.id}/'
        valid_assessment_name['name'] = 'new survey'
    
        response = client.patch(url, valid_assessment_name)
        self.assertEqual(response.data['name'], valid_assessment_name['name'])


    def test_delete_assessment_succeeds(self):
        client = APIClient()
        new_assessment_name =  TestFixtures.new_assessment_name()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/{new_assessment_name.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
