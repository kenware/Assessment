from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient

from django.contrib.auth.models import User


#mock
from .mocks.userMock import valid_user
base_url = 'http://127.0.0.1:8000/api/v1'
class UserEndpointsTests(APITestCase):
    def test_create_new_user_succeeds(self):      

        url = base_url + '/users/'
        response = self.client.post(url, valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'kenney')
        self.assertEqual(response.data['last_name'], 'keny')
        self.assertEqual(response.data['email'], 'kennedy@gmail.com')
        self.assertIn('token', response.data)

    def test_create_user_with_already_existing_email_and_username_fails(self):
        
        TestFixtures.new_user()
        url = base_url + '/users/'
        response = self.client.post(url, valid_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')

    def test_get_user_without_token_fails(self):
        
        url = base_url + '/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_user_succeeds(self):
        
        client = APIClient()
        TestFixtures.list_of_user()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        url = base_url + '/users/'
        response = client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreaterEqual(len(response.data['results']), 5)
    
    def test_update_user_succeeds(self):
        client = APIClient()
        new_user = TestFixtures.new_user()

        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/users/{new_user.id}/'
        valid_user['is_staff'] = True
        valid_user['firstName'] = 'Ejike'
        response = client.patch(url, valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'kenney')
        self.assertEqual(response.data['last_name'], 'keny')
        self.assertEqual(response.data['first_name'], 'Ejike')
        self.assertEqual(response.data['email'], 'kennedy@gmail.com')

    def test_user_user_succeeds(self):
        client = APIClient()
        new_user = TestFixtures.new_user()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token) 

        url = base_url + f'/users/{new_user.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    


              