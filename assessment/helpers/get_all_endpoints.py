
from assessment.helpers.query_parser import QueryParser

def get_paginated_and_query_filtered_data(model, schema, EagerLoadSchema):
    def list(self, request):
        url_query = request.query_params
        data = QueryParser.parse_all(self, model, url_query, schema, EagerLoadSchema)
        return data
    return list
