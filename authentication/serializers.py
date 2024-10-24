from rest_framework import serializers
from .models import *
import re

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id","email","first_name","last_name","password","confirm_password"]
        extra_kwargs = {
            "username" : {"read_only":True},
            "password" : {"write_only":True},
            "confirm_password" : {"write_only":True}
            }
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        role = attrs.get('role')
        
        if not role:
            raise serializers.ValidationError({"role" : "User Role must be required"})
        
        if not re.search(['A-Z'],password) == None and re.search(['a-z'],password) == None and re.search(['0-9'],password) == None and len(password) < 8:
            raise serializers.ValidationError({"password":"Password Must be Strong atleast 8 digit is required included digit is a number and character"})
        
        if not confirm_password:
            raise serializers.ValidationError({"confirm_password" : "Confirm Password is required"})

        if password != confirm_password:
            raise serializers.ValidationError({"password" : "Password And Confirm Password not match"})
        
        return attrs
    
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["email","password"]
        
    def get_password(self,obj):
        print(obj)
        pass