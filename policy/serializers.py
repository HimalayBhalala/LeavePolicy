from rest_framework import serializers
from .models import *

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ["user","name","created_at","updated_at"]

    def validate(self, attrs):
        name = attrs.get('name')
        check_exists = LeaveType.objects.filter(name=name)
        if check_exists.exists():
            raise serializers.ValidationError({"name":f" {self.name} type of Leave already exists"})
        return attrs
    
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return LeaveType.objects.create(**validated_data)