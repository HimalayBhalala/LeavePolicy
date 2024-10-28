from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from authentication.models import User

class JWTAuthentication(BasePermission):
    
    @staticmethod
    def decode_token_for_user(token):
        try:
            print("Helo")
            decode_token = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=settings.SIMPLE_JWT['ALGORITHM'])
            return decode_token['user_id']
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None


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
        
    def has_permission(self, request,view):
        user = self.authenticate(request)
        request.user = user
        return user is not None