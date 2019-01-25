from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import TestFixtures
from rest_framework.test import APIClient

from assessment.models import Answer
client = APIClient()
from assessment.middlewares.validators.messages import error_messages

#mock
from .mocks.answer_mock import choice, correct_choice

base_url = 'http://127.0.0.1:8000/api/v1'
class AnswerEndpointsTests(APITestCase):
    def test_create_new_answer_succeeds(self):      

        url = base_url + '/answers/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()

        correct_choice['questionId'] = question.id
        response = client.post(url, correct_choice)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['choice_text'], correct_choice['choiceText'])
    
    def test_non_multichoice_question_should_have_one_correct_answer(self):      

        url = base_url + '/answers/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        question = TestFixtures.new_question_object()
        Answer(choice_text='my answers', is_correct_choice=True, questions_id=question.id).save()

        correct_choice['questionId'] = question.id
        response = client.post(url, correct_choice)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], error_messages['answer_set'].format(question.id))
    
    def test_multichoice_question_should_have_many_correct_answer_succeeds(self):  

        url = base_url + '/answers/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        answer = TestFixtures.correct_choice()

        correct_choice['questionId'] = answer.questions_id
        response = client.post(url, correct_choice)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['choice_text'], correct_choice['choiceText'])

    def test_duplicate_choice_for_non_multichoice_questions_fails(self):
        url = base_url + '/answers/'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        answer = TestFixtures.choice()
        
        choice['choiceText'] = answer.choice_text
        choice['questionId'] = answer.questions_id
        response = client.post(url, choice)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], error_messages['choice_exist'].format(answer.questions_id))
    

    def test_create_answer_without_token_fails(self):
        
        url = base_url + '/answers/'
        response = self.client.post(url, correct_choice)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_answer_under_a_question_succeeds(self):
        
        question_id = TestFixtures.choice_list()
        url = base_url + f'/answers/?questionId={question_id}'
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)    
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreaterEqual(len(response.data['results']), 5)
    
    def test_update_answer_succeeds(self):
        client = APIClient()
        answer =  TestFixtures.choice()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)

        choice['questionId'] = answer.questions_id
        choice['isCorrectChoice'] = True
        url = base_url + f'/answers/{answer.id}/'
        response = client.patch(url, choice)
        self.assertEqual(response.data['answer']['choice_text'], choice['choiceText'])
        self.assertEqual(response.data['message'], 'Answer successfully updated')


    def test_delete_answer_succeeds(self):
        client = APIClient()
        answer =  TestFixtures.choice()
        token = 'Bearer ' + TestFixtures.auth_token()
        client.credentials(HTTP_AUTHORIZATION=token)
        url = base_url + f'/questions/{answer.id}/'
    
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
    


              