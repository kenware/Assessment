
from rest_framework import viewsets
from rest_framework.response import Response

class custom404(viewsets.ModelViewSet):
    
    def error_404(self, request):
        method = request.method
        return Response({
            'statusCode': 404,
            'error': f'The {method} request resource was not found'
        }, 404)

http_mapper = {
    'get': 'error_404',
    'post': 'error_404',
    'patch': 'error_404',
    'put': 'error_404',
    'delete': 'error_404',
}
