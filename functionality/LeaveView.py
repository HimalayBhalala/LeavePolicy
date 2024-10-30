from rest_framework.views import APIView
from .handle_exception import handle_internal_server_exception

class BaseAPIView(APIView):
    @handle_internal_server_exception
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
