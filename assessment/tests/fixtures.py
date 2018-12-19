from .mocks.userMock import valid_user
from django.contrib.auth.models import User
from assessment.helpers.token_generator import generate_token

class TestFixtures():
    def new_user():
        user = User(email=valid_user['email'], username=valid_user['username'])
        return user

    def auth_token():
        user = User(email='kenware@gmail.com', username='kenware2', is_staff=True)
        user.save()
        token = generate_token(user)
        return token

    def list_of_user():
        for n in range(5):
            user = User(email=valid_user['email'] + str(n), username=valid_user['username'] + str(n))
            user.save()