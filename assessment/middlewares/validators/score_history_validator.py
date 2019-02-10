
from assessment.middlewares.validators.errors import raises_error
def check_index(list, index):
    if index < 0:
        return False
    try:
        list[index]
        return True
    except IndexError:
        return False

def get_paginated_history(*args):
    scores, page_number, assessment_id, user_id, request = args
    page_number = int(page_number)
    index = page_number - 1
    base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)

    if check_index(scores, index):
        score = scores[index]

    else:
        raises_error('page_error', 404)

    prev = f'{base_url}?userId={user_id}&assessmentId={assessment_id}&page={page_number-1}' if check_index(scores, index-1) else 'null'
    next = f'{base_url}?userId={user_id}&assessmentId={assessment_id}&page={page_number+1}' if check_index(scores, index+1) else 'null'
    return prev, next, score 