from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from functionality.jsonrenderer import NewJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

def get_token_for_user(user):
    token = RefreshToken.for_user(user)

    return {
        "access_token":str(token.access_token),
        "refresh_token":str(token)
    }

class RegisterView(APIView):
    
    # renderer_classes = [NewJSONRenderer]/
    
    def post(self,request,*args,**kwargs):
        try:
            serializer_data = UserSerializer(data=request.data)
            if serializer_data.is_valid():
                user = serializer_data.save()

                token = get_token_for_user(user)

                return Response({
                    "message":"User Register Successfully...",
                    "data" : serializer_data.data,
                    "token" : token,
                    "status" : status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)
            
            return Response({
                "message":serializer_data.errors,
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):

    
    def get(self,request, *args, **kwargs):
        
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
          
        serializer_data = UserSerializer(request.data)
        
        try:                
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
                 
        except Exception as e:
            return Response({
                "message":str(e),
                "data":[],
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)