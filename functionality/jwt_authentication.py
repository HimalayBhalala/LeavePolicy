from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from authentication.models import User

class JWTAuthnetication(BasePermission):
    
    @staticmethod
    def decode_token_for_user(token):
        try:
            decode_token = jwt.decode(token,key=settings.SECRET_KEY,algorithms=['HS256'])
        except:
            decode_token = None
        return decode_token
    
    
    def authenticate(self,request):
        auth_token = request.headers.get('Authorization')
        
        if not auth_token:
            return None
        
        token = auth_token.split(' ')[-1]
        user_id = self.decode_token_for_user(token)
        try:
            user = User.objects.filter(id=user_id).first()
            return user
        except User.DoesNotExist:
            return None
        
    def has_permission(self, request):
        user = self.authenticate(request)
        request.user = user
        return user is not None