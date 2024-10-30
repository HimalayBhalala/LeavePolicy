from django.shortcuts import render
from rest_framework import status
from functionality.jwt_authentication import JWTAuthentication
from rest_framework.response import Response
from .models import *
from .serializers import *
from functionality.LeaveView import BaseAPIView
from functionality.jsonrenderers import LeaveJsonRenderer

# Leave Type Views
class LeaveTypeView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]

    def post(self,request,*args, **kwargs):

        user = request.user
        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        serializer_data = LeaveTypeSerializer(data=request.data,context={'user':user})

        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message":"LeaveType added Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_201_CREATED
            },status=status.HTTP_201_CREATED)
    
    def put(self,request,*args, **kwargs):
        id = self.kwargs.get('pk',None)
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        get_data = LeaveType.objects.filter(user=user,id=id).first()

        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveTypeSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message":"Leave Type updated Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)

     
    def delete(self,request,*args, **kwargs):

        id = self.kwargs.get('pk',None)
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)        
        
        user = request.user
      
        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        get_data = LeaveType.objects.filter(user=user,id=id).first()

        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)
        
        get_data.delete()

        return Response({
            "message":"Leave Type deleted successfully....",
            "data":[],
            "status":status.HTTP_204_NO_CONTENT
        },status=status.HTTP_204_NO_CONTENT)
      
class GetAllLeaveTypeView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    """ Get a all Leave Type"""

    def get(self,request,*args, **kwargs):
        data = LeaveType.objects.all()
        serialize_data = LeaveTypeSerializer(data,many=True)
        return Response({
            "message":"Leave Type getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)


# Leave Reason Views

class LeaveReasonView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]

    def post(self,request,*args, **kwargs):
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        serializer_data = LeaveReasonSerializer(data=request.data,context={'user':user})
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message":"LeaveReason Added Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_201_CREATED
            },status=status.HTTP_201_CREATED)


    def put(self,request,*args, **kwargs):
        id = self.kwargs.get('pk',None)
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        get_data = LeaveReason.objects.filter(user=user,id=id).first()
        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveReasonSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message":"Leave Reason updated Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)

    def delete(self,request,*args, **kwargs):

        id = self.kwargs.get('pk',None)
        
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        get_data = LeaveReason.objects.filter(user=user,id=id).first()

        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)
        
        get_data.delete()

        return Response({
            "message":"Leave Reason deleted successfully....",
            "data":[],
            "status":status.HTTP_204_NO_CONTENT
        },status=status.HTTP_204_NO_CONTENT)
    
class GetAllLeaveReasonView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]

    """ Get a all Leave Reason"""

    def get(self,request,*args, **kwargs):
        data = LeaveReason.objects.all()
        serialize_data = LeaveReasonSerializer(data,many=True)
        return Response({
            "message":"Leave Reason getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)

# Leave Rule Views
class LeaveRuleView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]

    def post(self,request,*args, **kwargs):
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
            
        serializer_data = LeaveRuleSerializer(data=request.data,context={'user':user})
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message" : "LeaveRule Added Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_201_CREATED
            },status=status.HTTP_201_CREATED)

    def put(self,request,*args, **kwargs):
        id = self.kwargs.get('pk',None)
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        get_data = LeaveRule.objects.filter(user=user,id=id).first()
        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveRuleSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({
                "message":"Leave Rule updated Successfully...",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)


    def delete(self,request,*args, **kwargs):

        id = self.kwargs.get('pk',None)
        
        if not id:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        get_data = LeaveRule.objects.filter(user=user,id=id).first()

        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)
        
        get_data.delete()

        return Response({
            "message":"Leave Rule deleted successfully....",
            "data":[],
            "status":status.HTTP_204_NO_CONTENT
        },status=status.HTTP_204_NO_CONTENT)

class GetAllLeaveRuleView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]

    """ Get a all Leave Rules"""

    def get(self,request,*args, **kwargs):
        data = LeaveRule.objects.all()
        serialize_data = LeaveRuleSerializer(data,many=True)
        return Response({
            "message":"Leave Rule getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)
        

