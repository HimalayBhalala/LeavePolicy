from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from functionality.LeaveView import BaseAPIView

# Create your views here.

def get_token_for_user(user):
    
    token = RefreshToken.for_user(user)

    return {
        "access_token":str(token.access_token),
        "refresh_token":str(token)
    }

class RegisterView(BaseAPIView):
            
    def post(self,request,*args,**kwargs):
        serializer_data = UserSerializer(data=request.data)
        try:
            if serializer_data.is_valid():

                user = serializer_data.save()
                token = get_token_for_user(user)

                return Response({
                    "message":"User Register Successfully...",
                    "data" : serializer_data.data,
                    "token" : token,
                    "status" : status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response
            
class LoginView(BaseAPIView):
        
    def get(self,request, *args, **kwargs):
        
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
          
        serializer_data = UserSerializer(request.data)
        
            
        user = User.objects.filter(email=email).first()
        
        if not role or user.role != role:
            return Response({
                "message":"Given role is not exists for user",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        if not user:
            return Response({
                "message":"User Not Found",
                "data":[],
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