from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from functionality.LeaveView import BaseAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

# Create your views here.

def get_token_for_user(user):
    
    token = RefreshToken.for_user(user)

    return {
        "access_token":str(token.access_token),
        "refresh_token":str(token)
    }

class RegisterView(BaseAPIView):
            
    def post(self,request,*args,**kwargs):
        try:
            serializer_data = UserSerializer(data=request.data)
            if serializer_data.is_valid(raise_exception=True):

                user = serializer_data.save()
                token = get_token_for_user(user)

                return Response({
                    "message":"User Register Successfully...",
                    "data" : serializer_data.data,
                    "token" : token,
                    "status" : status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                "message": e.detail,
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
            
class LoginView(BaseAPIView):
        
    def post(self,request, *args, **kwargs):
        
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
          
        serializer_data = UserSerializer(request.data)
            
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({
                "message":"User Not Found",
                "data":[],
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)  
          
        if not role or user.role != role:
            return Response({
                "message":"Given role is not exists for user",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
                        
        if user.check_password(password):

            token = get_token_for_user(user)

            return Response({
                "message":"User Login Successfully...",
                "data": serializer_data.data,
                "token":token,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        
        return Response({
            "message":"Enter a Valid Password",
            "status":status.HTTP_400_BAD_REQUEST
        },status=status.HTTP_400_BAD_REQUEST)