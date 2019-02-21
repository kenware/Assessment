from rest_framework.response import Response

from assessment.middlewares.validators.errors import raises_error
from re import sub
from assessment.middlewares.validators.constants import database_types, related_mapper

class QueryParser():
    valid_include = ['children']
    excluded_fields = ['score', 'questions', 'answers','correct_choices']
    included_params = ['include', 'order_by', 'assessment_id', 'question_id', 'page', 'user_id', 'assessment_name_id']
    related_mapper = related_mapper

    @classmethod
    def parse_all(cls, *args):
        self, model, query, schema, eagerLoadSchema=args
        querySet = cls.build_queryset(model, query)
        page = self.paginate_queryset(querySet)# if query.get('page') else None
        if page is not None:
            querySet = page

        schema_data = schema(querySet, many=True).data
        if eagerLoadSchema:
            schema_data = cls.include_children(schema, eagerLoadSchema, query, querySet, True)
        return cls.pagination_parser(self, page, schema_data)

    @classmethod
    def pagination_parser(cls, self, page, data):
        if page is not None:
            return self.get_paginated_response(data)
        return Response(data)

    @classmethod
    def include_children(cls, *args):
        schema, eagerLoadSchema, query, querySet, many = args
        include = query.get('include')
        if include:
            cls.validate_include(include)
            return eagerLoadSchema(querySet, many=many).data
        return schema(querySet, many=many).data
    
    @classmethod
    def validate_include(cls, include):
        if not include in cls.valid_include:
            raises_error('include_error', 400, include, cls.valid_include)

    @classmethod
    def build_queryset(cls, model, query):
        url_queries ={}
        order_by = query.get('orderBy')
        for key in query.keys():
            url_queries.update(cls.query_to_dict(key, query, model))
            url_queries = cls.filter_by_related_id(model.__name__, key, query, url_queries)
        if order_by:
            order = cls.validate_order_by(order_by, model)
            return model.objects.filter(**url_queries).order_by(order)
        return model.objects.filter(**url_queries)
    
    @classmethod
    def filter_by_related_id(cls, *args):
        model_name, key, query, url_query = args
        related_data = cls.related_mapper.get(key)
        if related_data and related_data.get(model_name):
            related_id_value = query.get(key)
            cls.validate_field_type('IntegerField', related_id_value)
            url_query.update({related_data[model_name]: related_id_value})
        elif related_data:
            raises_error('url_query_error', 400, key, model_name)
        return url_query

    @classmethod
    def get_model_fields(cls, model):
        valid_fields = {field.name:field.get_internal_type() for field in model._meta.get_fields() if field.name not in cls.excluded_fields}
        return valid_fields
 
    @classmethod
    def query_to_dict(cls, key, query, model):
        snake_case_key = cls.snake_case(key)
        model_fields = cls.get_model_fields(model)
        url_query_value = query.get(key)
        if snake_case_key in model_fields:
            model_type = model_fields[snake_case_key]
            cls.validate_field_type(model_type,url_query_value)
            return { snake_case_key: url_query_value }
        if snake_case_key[6:] in model_fields or snake_case_key[4:] in model_fields:
            return cls.start_end_query_to_dict(snake_case_key, url_query_value)
        if snake_case_key in cls.included_params:
            return {}
        raises_error('url_query_error', 400, key, model.__name__)

    @classmethod
    def snake_case(cls, string):
        return sub(r'(.)([A-Z])', r'\1_\2', string).lower()
    
    @classmethod
    def validate_field_type(cls, model_type, value):
        try:
            get_type = database_types.get(str(model_type))
            if get_type:
               (get_type.get('cast')(value))

        except ValueError: 
            raises_error('invalid_value', 400, value, model_type, )

    @classmethod
    def start_end_query_to_dict(cls, key, value):
        if key.startswith('start'):
            return { f'{key[6:]}__gte': value }
        elif key.startswith('end'):
            return { f'{key[4:]}__lte': value }
        return {}
        
    
    @classmethod
    def validate_order_by(cls, order_by, model):
        order_by_colunm = cls.snake_case(order_by)
        colunm = order_by_colunm[4:]
        if not colunm in cls.get_model_fields(model):
            raises_error('order_by_error', 400, order_by, 'orderBy')
        
        if order_by.startswith('dec'):
            return f'-{colunm}'
        if order_by.startswith('asc'):
            return colunm
        raises_error('order_by_error', 400, order_by, 'orderBy')
