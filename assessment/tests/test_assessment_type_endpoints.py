from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient

from assessment.models import Assessment
client = APIClient()

#mock
from .mocks.userMock import valid_assessment

base_url = 'http://127.0.0.1:8000/api/v1'
class AssessmentTypeEndpointsTests(APITestCase):
    def test_create_new_assessment_succeeds(self):      
        name = TestFixtures.new_assessment_name()
        valid_assessment['nameId'] = name.id

        url = base_url + '/assessments/type/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        
        response = client.post(url, valid_assessment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], valid_assessment['type'])
        self.assertEqual(response.data['max_time'], '00:00:01')

    def test_create_assessment_with_already_existing_name_and_assessment_type_fails(self):
        
        url = base_url + '/assessments/type/'
        assessment = TestFixtures.new_assessment_object()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        
        valid_assessment['nameId'] = assessment.name_id

        response = client.post(url, valid_assessment)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'This assessment type already exist in this assessment')

    def test_create_assessment_without_token_fails(self):
        
        url = base_url + '/assessments/type/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_assessments_succeeds(self):
        
        url = base_url + '/assessments/type/'
        TestFixtures.new_assessment().save()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertIsInstance(response.data, dict)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_update_assessment_succeeds(self):
        client = APIClient()
        new_assessment =  TestFixtures.new_assessment_object()
   
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/type/{new_assessment.id}/'
        valid_assessment['type'] = 'new survey'
        valid_assessment['nameId'] = new_assessment.name_id
        response = client.patch(url, valid_assessment)
        self.assertEqual(response.data['type'], valid_assessment['type'])
        self.assertEqual(response.data['max_time'], '00:00:01')

    def test_delete_assessment_succeeds(self):
        client = APIClient()
        new_assessment =  TestFixtures.new_assessment_object()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/type/{new_assessment.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    


              