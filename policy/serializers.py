from rest_framework import serializers
from .models import LeaveRequest
from leavepolicyrules.models import *
from datetime import date,timedelta

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["id","leave_type","custom_leave","leave_rule","leave_reason","leave_description","status","approved_by","requested_date","created_at","updated_at"]

    def validate(self, attrs):
        leave_type = attrs.get('leave_type')
        leave_reason = attrs.get('leave_reason')
        leave_rule = attrs.get('leave_rule')
        user = self.context.get('user')
        requested_date = attrs.get('requested_date')

        get_leave_type = LeaveType.objects.filter(id=leave_type.id).first()
        get_leave_reason = LeaveReason.objects.filter(id=leave_reason.id).first()
        get_leave_rule = LeaveRule.objects.filter(id=leave_rule.id).first()
        
        if not get_leave_reason.leave_type.id == get_leave_type.id:
            raise serializers.ValidationError({"leave_reason":"Leave reason is not exists in given leave_type"})    

        if get_leave_reason.leave_type.id == get_leave_type.id and get_leave_reason.reason == "Custom":
            custom_leave = attrs.get('custom_leave')
            if not custom_leave:
                raise serializers.ValidationError({"custom_leave_reason":"Custom Leave Reason is required"})

        if not get_leave_rule.role == user.role:
            raise serializers.ValidationError({"role":"Add a right role"})

        leave_request_date = date.today() + timedelta(days=get_leave_rule.days)
        print(leave_request_date,requested_date)
        if (get_leave_rule.role == user.role) and (leave_request_date > requested_date):
            raise serializers.ValidationError({"leave_request":"You have not able to get a leave because your request days is over"})
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return LeaveRequest.objects.create(**validated_data)
    

class LeaveRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["id","leave_type","custom_leave","leave_rule","leave_reason","leave_description","status","approved_by","requested_date","created_at","updated_at"]

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status',instance.status)
        instance.approved_by = self.context.get('user',instance.approved_by)
        instance.save()
        return instance
