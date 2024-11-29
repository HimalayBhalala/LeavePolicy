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
from functionality.permission import HrOrAdmin,AdminOrHrOrPmOrTl

class LeaveRequestView(APIView):

    """ Include LeaveRequestView """

    # renderer_classes = [LeaveJsonRenderer]
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

    """ Include GetAllLeaveRequest"""

    renderer_classes = [LeaveJsonRenderer]
          
    def get(self,request,*args, **kwargs):
        data = LeaveRequest.objects.all().order_by('-id')
        serialize_data = LeaveRequestSerializer(data,many=True)
        return Response({
            "message":"Leave Request getted successfully....",
            "data":serialize_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)

class ApprovedRequestView(BaseAPIView):

    permission_classes = [JWTAuthentication,AdminOrHrOrPmOrTl]
    renderer_classes = [LeaveJsonRenderer]

    def put(self,request,*args, **kwargs):
        
        try:
            user = request.user
            
            id = self.kwargs.get('pk',None)
            if id is None:
                return Response({
                    "message":"Id is required in URl",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)
            
            get_request = LeaveRequest.objects.get(id=id)
            if get_request.admin_status==0:
                return Response({
                        "message":f"This request is rejected by admin - {get_request.approved_by_admin}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)

            elif get_request.admin_status==1:
                    return Response({
                        "message":f"This request is already approved by admin - {get_request.approved_by_admin}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)

            # Check for approved leaveRequest
            elif get_request.user.role == 'developer':
                # Check for rejected leaveRequest
                if get_request.hr_status==0:
                    return Response({
                        "message":f"This request is rejected by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif get_request.pm_status==0:
                    return Response({
                        "message":f"This request is rejected by pm - {get_request.approved_by_pm}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif get_request.tl_status==0:
                    return Response({
                        "message":f"This request is rejected by tl - {get_request.approved_by_tl}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                

                if get_request.hr_status==1:
                    return Response({
                        "message":f"This request is already approved by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif (get_request.pm_status==2 and get_request.tl_status==2) and not user.role in ['admin','hr','pm','tl']:
                     return Response({
                        "message":"Admin,Hr,Pm Or Tl leaverequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif (get_request.pm_status==2) and not user.role in ['admin','hr','pm']:
                    return Response({
                        "message":"Admin,Hr Or Pm leaverequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif (get_request.pm_status==1) and not user.role in ['admin','hr']:
                    return Response({
                        "message":"Admin Or Hr leaveRequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                
            elif get_request.user.role == 'tl':
                if get_request.hr_status==0:
                    return Response({
                        "message":f"This request is rejected by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif get_request.pm_status==0:
                    return Response({
                        "message":f"This request is rejected by pm - {get_request.approved_by_pm}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)

                if get_request.hr_status==1:
                    return Response({
                        "message":f"This request is already approved by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif get_request.pm_status==2 and not user.role in ['admin','hr','pm']:
                    return Response({
                        "message":"Admin,Hr Or Pm leaverequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif get_request.pm_status==1 and not user.role in ['admin','hr']:
                    return Response({
                        "message":"Admin Or Hr leaveRequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                
            elif get_request.user.role == 'pm':
                if get_request.hr_status==0:
                    return Response({
                        "message":f"This request is rejected by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                
                if get_request.hr_status==1:
                    return Response({
                        "message":f"This request is already approved by hr - {get_request.approved_by_hr}",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                elif not user.role in ['admin','hr']:
                    return Response({
                        "message":"Admin Or Hr leaveRequest approvel is required",
                        "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_400_BAD_REQUEST)
                
            elif get_request.user.role == 'hr':
                if not user.role == 'admin':
                    return Response({
                        "message":"Admin leaveRequest approvel is required",
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
        filter_query = []

        leave_admin_status = request.GET.get('admin_status', '').strip() 
        leave_hr_status = request.GET.get('hr_status', '').strip()
        leave_pm_status = request.GET.get('pm_status', '').strip()
        leave_tl_status = request.GET.get('tl_status', '').strip()
        leave_description = request.GET.get('description', '').strip()
        leave_type = request.GET.get('leave_type', '').strip()
        leave_reason = request.GET.get('leave_reason', '').strip()
        created_start_date = request.GET.get('created_start_date',None)
        created_end_date = request.GET.get('created_end_date',None)
        
        if leave_admin_status:
            filter_query.append(Q(admin_status__icontains=leave_admin_status))
        
        if leave_hr_status:
            filter_query.append(Q(hr_status__icontains=leave_hr_status))

        if leave_pm_status:
            filter_query.append(Q(pm_status__icontains=leave_pm_status))

        if leave_tl_status:
            filter_query.append(Q(tl_status__icontains=leave_tl_status))

        if leave_description:
            filter_query.append(Q(leave_description__icontains=leave_description))

        if leave_type:
            filter_query.append(Q(leave_type__name__icontains=leave_type))

        if leave_reason:
            filter_query.append(Q(leave_reason__reason__icontains=leave_reason))

        final_formated_start_date = timezone.now() - timedelta(days=30)
        final_formated_end_date = timezone.now()
        
        if created_start_date:
            formated_start_date = datetime.strptime(created_start_date,'%d-%m-%Y')
            final_formated_start_date = formated_start_date.strftime('%Y-%m-%d')

        if created_end_date:
            formated_end_date = datetime.strptime(created_end_date,"%d-%m-%Y")
            final_formated_end_date = formated_end_date.strftime("%Y-%m-%d")

        filter_query.append(Q(created_at__date__range=(final_formated_start_date,final_formated_end_date)))
        
        request_data = LeaveRequest.objects.filter(user=user,*filter_query)
        serializer_data = LeaveRequestSerializer(request_data,many=True)

        return Response({
            "message":"Filtered data is getting successfully....",
            "data":serializer_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)


class DeleteLeaveRequestView(BaseAPIView):
    
    permission_classes = [JWTAuthentication,HrOrAdmin]
    renderer_classes = [LeaveJsonRenderer]
    
    def delete(self,request,*args, **kwargs):

        id = self.kwargs.get('pk',None)
        if id is None:
            return Response({
                "message":"Id is required in URl",
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        get_request = LeaveRequest.objects.filter(id=id)
        
        if not get_request.exists():
            return Response({
                "message":"No Data found....",
                "data":[],
                "status":status.HTTP_204_NO_CONTENT
            },status=status.HTTP_204_NO_CONTENT)
        
        get_request.delete()

        return Response({
            "message":"LeaveRequest deleted successfully...",
            "data":[],
            "status":status.HTTP_204_NO_CONTENT            
        },status=status.HTTP_204_NO_CONTENT)


class CheckAllApprovedRequest(BaseAPIView):
    
    permission_classes = [JWTAuthentication]
    renderer_classes = [LeaveJsonRenderer]

    def get(self,request,*args, **kwargs):
        user = request.user

        approved_requests = LeaveRequest.objects.filter(user=user).filter(Q(hr_status=1) | Q(admin_status=1)).order_by('-id')

        serialized_data = LeaveRequestSerializer(approved_requests,many=True)

        return Response({
            "message":"Approved leaverequest getting successfully... ",
            "data":serialized_data.data,
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK)
