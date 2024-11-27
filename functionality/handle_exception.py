from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def handle_internal_server_exception(fun):
    @wraps(fun)
    def get_exception(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        
        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return get_exception