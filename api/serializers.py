from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework.exceptions import AuthenticationFailed
from .models import User




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','password2','is_doctor']


        def validate(self,data):
            password = data.get('password')
            password2 = data.get('password2')

            if password != password2:
                raise serializers.ValidationError("password doesnt match")
            
            elif len(password)<8:
                raise serializers.ValidationError("Password must need 8 charecters")
            
            return data
        
        def validate_email(self,value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email address is already in use")
            return value
        
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        token['blocked'] = user.blocked
        return token

    def validate(self, attrs):
        data =  super().validate(attrs)     
        user = self.user

        if user.is_blocked:
            raise AuthenticationFailed("Your accounts is blocked due to some reason, Please contact admin")
        
        return data
    