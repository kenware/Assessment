from rest_framework import serializers
from assessment.middlewares.validators.messages import error_messages


def raises(error_key, status_code, *args, **kwargs):
    """
    Raises a serialization error

    Parameters:
        error_key (str): the key for accessing the correct error message
        args (*): variable number of arguments
        kwargs (**): variable number of keyword arguments
    """

    raise serializers.ValidationError(
         error_messages[error_key].format(*args, **kwargs),
         status_code)

def raises_error(error_key, status_code, *args, **kwargs):
    """
    Raises a serialization error

    Parameters:
        error_key (str): the key for accessing the correct error message
        args (*): variable number of arguments
        kwargs (**): variable number of keyword arguments
    """

    raise serializers.ValidationError({
         'message': error_messages[error_key].format(*args, **kwargs),
         'status': 'error'})