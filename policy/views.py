from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView 
from functionality.jwt_authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import *
from .serializers import *


# Create your views here.

class LaveTypeView(APIView):

    permission_classes = [JWTAuthentication,IsAdminUser]

    def post(self,request,*args, **kwargs):

        try:
            user = request.user
            serializer_data = LeaveTypeSerializer(data=request.data,context={'user':user})

            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()

                return Response({
                    "message":"LeaveType added Successfully...",
                    "data":serializer_data.data,
                    "status":status.HTTP_201_CREATED
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
        

class GetAllLeaveTypeView(APIView):

    def get(self,request,*args, **kwargs):
        try:
            data = LeaveType.objects.all()
            print(data)
            serialize_data = LeaveTypeSerializer(data,many=True)
            return Response({
                "message":"Leave Type getted successfully....",
                "data":serialize_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
