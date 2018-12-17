# user schema
from assessment.serializers.user import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    """ custmoze jwt payload data

       Args:
         token (str): incoming token
         user (obj): User object
         request (obj): Request object
    """
     
    user = UserSerializer(user, context={'request': request}).data
    user['token'] = token
    return user