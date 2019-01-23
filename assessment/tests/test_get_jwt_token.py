from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient
from django.contrib.auth.models import User

client = APIClient()

#mock
from .mocks.userMock import valid_user
base_url = 'http://127.0.0.1:8000/api/v1'

class GetJwtEndpointsTests(APITestCase):
    def test_get_jwt_token_with_valid_user_succeeds(self):
        user = User.objects.create(username='kenny')
        user.set_password('12345')
        user.save()
        url = base_url + '/login/'
        response = client.post(url, {'username': 'kenny', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'kenny')
        self.assertIsInstance(response.data['token'], str)
