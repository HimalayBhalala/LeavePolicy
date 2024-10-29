from rest_framework import serializers
from .models import *

# Leave Type Serializer
class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ["id","user","name","created_at","updated_at"]
        extra_kwargs = {
            "id":{"read_only":True},
        }
    def validate(self, attrs):
        name = attrs.get('name')
        check_exists = LeaveType.objects.filter(name=name)
        if check_exists.exists():
            raise serializers.ValidationError({"name":f" {name} type of Leave already exists"})
        return attrs
    
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return LeaveType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance
    

# Leave Reason Serializer

class LeaveReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReason
        fields = ["id","user","leave_type","reason","created_at","updated_at"]

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return LeaveReason.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.leave_type = validated_data.get('leave_type',instance.leave_type)
        instance.reason = validated_data.get('reason',instance.reason)
        instance.save()
        return instance
    

class LeaveRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRule
        fields = ["id","user","days","created_at","role","updated_at"]

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return LeaveRule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.days = validated_data.get('days',instance.days)
        instance.role = validated_data.get('role',instance.role)
        instance.save()
        return instance
