from django.shortcuts import render
from rest_framework import status
from .models import *
from .serializers import LeaveRequestSerializer,LeaveRequestStatusUpdateSerializer
from rest_framework.views import APIView
from functionality.jwt_authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class LeaveRequestView(APIView):

    permission_classes = [JWTAuthentication]
    
    def post(self,request,*args, **kwargs):
        user = request.user
        try:
            serializer_data = LeaveRequestSerializer(data=request.data,context={'user':user})
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                return Response({
                    "message":"Request Sent Successfully",
                    "data":serializer_data.data,
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                "message":e.detail,
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAllLeaveRequestView(APIView):
     
     def get(self,request,*args, **kwargs):
        try:
            data = LeaveRequest.objects.all()
            serialize_data = LeaveRequestSerializer(data,many=True)
            return Response({
                "message":"Leave Request getted successfully....",
                "data":serialize_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ApprovedRequestView(APIView):

    permission_classes = [JWTAuthentication,IsAdminUser]

    def put(self,request,*args, **kwargs):
        
        try:
            id = self.kwargs.get('pk',None)
            user = request.user

            if not id:
                return Response({
                    "message":"Id is required in URl",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)
            
            get_request = LeaveRequest.objects.get(id=id)
            serializer_data = LeaveRequestStatusUpdateSerializer(get_request,data=request.data,context={'user':user},partial=True)

            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                return Response({
                    "message":"Leave Request Updated successfully...",
                    "data":serializer_data.data,
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                "message":e.detail,
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        except LeaveRequest.DoesNotExist:
            return Response({
                "message":"Leave Request is not exists",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message":str(e),
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)