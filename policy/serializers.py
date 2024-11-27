from rest_framework import serializers
from .models import LeaveRequest
from leavepolicyrules.models import *
from datetime import date,timedelta
from django.db.models import Q

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["id","user","leave_type","custom_leave","leave_rule","leave_reason","leave_description","admin_status","hr_status","pm_status","tl_status","approved_by_admin","approved_by_hr","approved_by_pm","approved_by_tl","total_days","start_date","end_date","created_at","updated_at","start_date","end_date"]
        extra_kwargs = {
            "user":{"read_only":True}
        }

    def validate(self, attrs):
        leave_type = attrs.get('leave_type')
        leave_reason = attrs.get('leave_reason')
        leave_rule = attrs.get('leave_rule')
        user = self.context.get('user')
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        get_leave_type = LeaveType.objects.filter(id=leave_type.id).first()
        get_leave_reason = LeaveReason.objects.filter(id=leave_reason.id).first()
        get_leave_rule = LeaveRule.objects.filter(id=leave_rule.id).first()
        
        if not start_date:
            raise serializers.ValidationError({'start_date':"Start Date must be required"})

        if not end_date:
            raise serializers.ValidationError({'end_date':"End Date must be required"})
        
        get_leave_request = LeaveRequest.objects.filter(user=user,start_date__lte=end_date,end_date__gte=start_date).filter(Q(hr_status=1) | Q(admin_status=1))

        if get_leave_request.exists():
            raise serializers.ValidationError({"leave_request":"Leave Request already exists"})

        if not get_leave_reason.leave_type.id == get_leave_type.id:
            raise serializers.ValidationError({"leave_reason":"Leave reason is not exists in given leave_type"})    

        if get_leave_reason.leave_type.id == get_leave_type.id and get_leave_reason.reason == "Custom":
            custom_leave = attrs.get('custom_leave')
            if not custom_leave:
                raise serializers.ValidationError({"custom_leave":"Custom Leave Reason is required"})

        if not get_leave_rule.role == user.role:
            raise serializers.ValidationError({"rule":"Add a right rule"})

        leave_request_date = date.today() + timedelta(days=get_leave_rule.days)
        if (get_leave_rule.role == user.role) and (leave_request_date > start_date):
            raise serializers.ValidationError({"leave_request":"You have not able to get a leave because your request days is over"})
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        validated_data['total_days'] = (end_date - start_date).days
        return LeaveRequest.objects.create(**validated_data)
    

class LeaveRequestStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(write_only=True)
    class Meta:
        model = LeaveRequest
        fields = ["id","user","leave_type","custom_leave","leave_rule","leave_reason","leave_description","admin_status","hr_status","pm_status","tl_status","status","approved_by_admin","approved_by_hr","approved_by_pm","approved_by_tl","total_days","start_date","end_date","created_at","updated_at"]
        extra_kwargs = {
            "user":{"read_only":True}
        }

    def validate(self, attrs):
        get_status = attrs.get('status')
        if not get_status:
            raise serializers.ValidationError({"status":"Status must be required"})
        return attrs


    def update(self, instance, validated_data):
        user = self.context.get('user')

        if user.role == 'admin':
            instance.approved_by_admin = self.context.get('user',instance.approved_by_admin)
            instance.admin_status = validated_data.get('status',instance.admin_status)
        elif user.role == 'hr':
            instance.approved_by_hr = self.context.get('user',instance.approved_by_hr)
            instance.hr_status = validated_data.get('status',instance.hr_status)
        elif user.role == 'pm':
            instance.approved_by_pm = self.context.get('user',instance.approved_by_pm)
            instance.pm_status = validated_data.get('status',instance.pm_status)
        elif user.role == 'tl':
            instance.approved_by_tl = self.context.get('user',instance.approved_by_tl)
            instance.tl_status = validated_data.get('status',instance.tl_status)

        instance.save()
        return instance
