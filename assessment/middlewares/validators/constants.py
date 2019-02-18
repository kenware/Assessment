
from datetime import datetime, time
from assessment.middlewares.validators.errors import raises_error
database_types = {
            'ArrayField': {
                'cast': list,
                'op': 'like'
            },
            'IntegerField': {
                'cast': int,
                'op': 'eq'
            },
            'BooleanField': {
                'cast': lambda value: boolean(value),
                'op': 'eq',
            },
            'DateField': {
                'cast': lambda value: datetime.strptime(value, '%Y-%m-%d'),
                'op': 'eq'
            },
            'DecimalField': {
                'cast': float,
                'op': 'like'
            },
            'CharField': {
                'cast': str,
                'op': 'eq'
            },
            'AutoField':  {
                'cast': int,
                'op': 'eq'
            },
            'TimeField': {
                'cast': lambda value: datetime.strptime(value, '%H:%M:%S'), 
                'op': 'eq'
            }, 
            'TextField': {
                'cast': str,
                'op': 'eq'
            },
        } 

def boolean(value):
    if not (value == 'True' or value == 'False'):
       raises_error('url_query_error', 400, value, 'BooleanField. Valid value is either True or False')

related_mapper = {
    'assessmentId': {
        'Question': 'assessments_id',
        'Score': 'assessments_id',
    },
    'questionId': {
        'Answer': 'questions_id'
    },
    'userId': {
        'Score': 'user_id'
    },
    'assessmentNameId': {
    'Score': 'assessments_id',
    }
    }