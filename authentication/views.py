from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from functionality.jsonrenderer import JsonRenderer

# Create your views here.

class RegisterView(APIView):
    
    renderer_classes = [JsonRenderer]
    
    def post(self,request,*args,**kwargs):
        try:
            print(request.data)
            serializer_data = UserSerializer(data=request.data)
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                return Response({
                    "message" : serializer_data.data,
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
