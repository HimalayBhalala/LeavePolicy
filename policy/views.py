from django.shortcuts import render
from rest_framework import status
from .models import *
from .serializers import LeaveRequestSerializer,LeaveRequestStatusUpdateSerializer
from functionality.jwt_authentication import JWTAuthentication
from rest_framework.response import Response
from functionality.handle_exception import *
from functionality.jsonrenderers import LeaveJsonRenderer
from functionality.LeaveView import BaseAPIView
from rest_framework.views import APIView
from django.db.models import Q
from datetime import timedelta,datetime
from django.utils import timezone

class LeaveRequestView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]
    
    def post(self,request,*args, **kwargs):
        user = request.user
        serializer_data = LeaveRequestSerializer(data=request.data,context={'user':user})
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return Response({
                "message":"Request Sent Successfully",
                "data":serializer_data.data,
                "status":status.HTTP_201_CREATED
            },status=status.HTTP_201_CREATED)

class GetAllLeaveRequestView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
          
    def get(self,request,*args, **kwargs):
        data = LeaveRequest.objects.all()
        serialize_data = LeaveRequestSerializer(data,many=True)
        return Response({
            "message":"Leave Request getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)

class ApprovedRequestView(BaseAPIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]

    def put(self,request,*args, **kwargs):
        
        try:
            id = self.kwargs.get('pk',None)
            user = request.user
            
            if id is None:
                return Response({
                    "message":"Id is required in URl",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)

            get_request = LeaveRequest.objects.get(id=id)
            
            if not user.role in ['admin','hr']:
                return Response({
                    "message":"Only admin and Hr can be able to update a leave status",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)
            elif get_request.user.role == 'hr' and not user.role == 'admin':
                return Response({
                    "message":"Only admin can be able to update a leave status",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)

            serializer_data = LeaveRequestStatusUpdateSerializer(get_request,data=request.data,context={'user':user},partial=True)

            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                return Response({
                    "message":"Leave Request Updated successfully...",
                    "data":serializer_data.data,
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            
        except LeaveRequest.DoesNotExist:
            return Response({
                "message":"Leave Request is not exists",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)
        

class FilterDataView(APIView):

    renderer_classes = [LeaveJsonRenderer]
    permission_classes = [JWTAuthentication]

    def get(self,request,*args, **kwargs):
        
        user = request.user

        leave_status = request.GET.get('status',None)
        leave_description = request.GET.get('description',None)
        leave_type = request.GET.get('leave_type', None)
        leave_reason = request.GET.get('leave_reason',None)
        start_date = request.GET.get('start_date',None)
        end_date = request.GET.get('end_date',None)
        
        filter_query = []

        if leave_status:
            filter_query.append(Q(status__icontains=leave_status.strip()))

        if leave_description:
            filter_query.append(Q(leave_description__icontains=leave_description.strip()))

        if leave_type:
            filter_query.append(Q(leave_type__name__icontains=leave_type.strip()))

        if leave_reason:
            filter_query.append(Q(leave_reason__reason__icontains=leave_reason.strip()))

        final_formated_start_date = timezone.now() - timedelta(days=1)
        final_formated_end_date = timezone.now()
        
        if start_date and end_date:
            formated_start_date = datetime.strptime(start_date,'%d-%m-%Y')
            formated_end_date = datetime.strptime(end_date,"%d-%m-%Y")

            final_formated_start_date = formated_start_date.strftime('%Y-%m-%d')
            final_formated_end_date = formated_end_date.strftime("%Y-%m-%d")

        filter_query.append(Q(created_at__date__range=(final_formated_start_date,final_formated_end_date)))
        
        request_data = LeaveRequest.objects.filter(user=user,*filter_query)
        serializer_data = LeaveRequestSerializer(request_data,many=True)

        return Response({
            "message":"Filtered data is getting successfully....",
            "data":serializer_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)
