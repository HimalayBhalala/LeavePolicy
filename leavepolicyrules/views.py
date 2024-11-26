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

        if serializer_data.is_valid():
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


        get_data = LeaveType.objects.filter(user=user,id=id,status=True).first()

        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveTypeSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid():
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
    
class ChangeLeaveTypeStatus(BaseAPIView):

    permission_classes = [JWTAuthentication]
    renderer_classes = [LeaveJsonRenderer]

    def put(self,request,*args, **kwargs):
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        id = request.data.get('id')

        if not id:
            return Response({
                "message":"LeaveType ID must be required",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        get_leave_type = LeaveType.objects.filter(user=user,id=id).first()

        if not get_leave_type:
            return Response({
                "message":"No data found with enter leave_type id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        serializer_data = LeaveTypeStatusSerializer(get_leave_type,data=request.data,context={'user':user},partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response({
                "message":"LeaveType Status Updated Successfully......",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)


class GetAllLeaveTypeView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    """ Get a all Leave Type"""

    def get(self,request,*args, **kwargs):
        data = LeaveType.objects.filter(status=True).order_by('name')
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
        if serializer_data.is_valid():
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

        get_data = LeaveReason.objects.filter(user=user,id=id,status=True).first()
        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveReasonSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid():
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
    

class ChangeLeaveReasonStatus(BaseAPIView):

    permission_classes = [JWTAuthentication]
    renderer_classes = [LeaveJsonRenderer]

    def put(self,request,*args, **kwargs):
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        id = request.data.get('id')

        if not id:
            return Response({
                "message":"LeaveReason ID must be required",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        get_leave_reason = LeaveReason.objects.filter(user=user,id=id).first()
        
        if not get_leave_reason:
            return Response({
                "message":"No data found with enter leave_reason id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        serializer_data = LeaveReasonStatusSerializer(get_leave_reason,data=request.data,partial=True)

        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response({
                "message":"LeaveReason Status Updated Successfully......",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        

    
class GetAllLeaveReasonView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]

    """ Get a all Leave Reason"""

    def get(self,request,*args, **kwargs):
        data = LeaveReason.objects.filter(status=True).order_by('reason')
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
        if serializer_data.is_valid():
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
        
        get_data = LeaveRule.objects.filter(user=user,id=id,status=True).first()
        if not get_data:
            return Response({
                "message":"Data not found",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)

        serializer_data = LeaveRuleSerializer(get_data,data=request.data,partial=True)
        if serializer_data.is_valid():
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


class ChangeLeaveRuleStatus(BaseAPIView):

    permission_classes = [JWTAuthentication]
    renderer_classes = [LeaveJsonRenderer]

    def put(self,request,*args, **kwargs):
        user = request.user

        if not user.role in ['admin','hr']:
            return Response({
                "message":"Only admin and Hr can be able to update a leave status",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


        id = request.data.get('id')

        if not id:
            return Response({
                "message":"LeaveRule ID must be required",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        get_leave_rule = LeaveRule.objects.filter(user=user,id=id).first()

        if not get_leave_rule:
            return Response({
                "message":"No data found with enter leave_reason id",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)

        serializer_data = LeaveRuleStatusSerializer(get_leave_rule,data=request.data,context={'user':user},partial=True)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response({
                "message":"LeaveRule Status Updated Successfully......",
                "data":serializer_data.data,
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        
        
class GetAllLeaveRuleView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]

    """ Get a all Leave Rules"""

    def get(self,request,*args, **kwargs):
        data = LeaveRule.objects.filter(status=True).order_by('days')
        serialize_data = LeaveRuleSerializer(data,many=True)
        return Response({
            "message":"Leave Rule getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)
        

