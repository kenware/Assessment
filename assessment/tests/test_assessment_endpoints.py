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

        url = base_url + '/assessments/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.post(url, valid_assessment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], valid_assessment['title'])
        self.assertEqual(response.data['max_time'], '00:00:01')

    def test_create_assessment_with_already_existing_title_and_username_fails(self):
        
        url = base_url + '/assessments/'
        TestFixtures.new_assessment().save()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        response = client.post(url, valid_assessment)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'][0], 'assessment with this title already exists.')

    def test_create_assessment_without_token_fails(self):
        
        url = base_url + '/assessments/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_assessments_succeeds(self):
        
        url = base_url + '/assessments/'
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
        new_assessment =  TestFixtures.new_assessment()
        TestFixtures.new_assessment().save()
        assessment = Assessment.objects.get(title=new_assessment.title) #pylint: disable=E1101
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/{assessment.id}/'
        valid_assessment['title'] = 'new survey'
        response = client.patch(url, valid_assessment)
        self.assertEqual(response.data['title'], valid_assessment['title'])
        self.assertEqual(response.data['max_time'], '00:00:01')

    def test_delete_assessment_succeeds(self):
        client = APIClient()
        new_assessment =  TestFixtures.new_assessment()
        TestFixtures.new_assessment().save()
        assessment = Assessment.objects.get(title=new_assessment.title) #pylint: disable=E1101
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/assessments/{assessment.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    


              