from rest_framework import serializers
from .models import *
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email","first_name","last_name","password","confirm_password","role"]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if len(password) < 8:
            raise serializers.ValidationError({"password":"Password contains atleast 8 digits"})

        if not confirm_password:
            raise serializers.ValidationError({"confirm_password" : "Confirm Password is required"})

        if password != confirm_password:
            raise serializers.ValidationError({"password" : "Password And Confirm Password not match"})
        
        return attrs
    
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)
        if user.role == 'admin':
            user.is_superuser=True
            user.is_staff = True
        elif user.role == 'hr':
            user.is_staff=True
        user.save()
        return user