from assessment.helpers.query_parser import QueryParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

def retrieve_filtered_data(model, schema, EagerLoadSchema):
    def retrieve(self, request, pk=None):
        url_query = request.query_params
        queryset = get_object_or_404(model, pk=pk)
        assessment_data = QueryParser.include_children(schema, EagerLoadSchema, url_query, queryset, False) 
        return Response(assessment_data)
    return retrieve
