from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework.exceptions import AuthenticationFailed,ValidationError
from .models import User,Doctors




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2','is_doctor']


        def validate(self,data):
            password = data.get('password')
            password2 = data.get('password2')

            length = len(password)

            if length<8:
                raise serializers.ValidationError("Password must need 8 charecters")
            
            if password != password2:
                raise serializers.ValidationError("password doesnt match")
            
            
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

        if user.blocked:
            raise AuthenticationFailed("Your accounts is blocked due to some reason, Please contact admin")
        
        return data


class DocterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors  
        fields = ["department","hospital","is_verified"]   


class UserListSerializer(serializers.ModelSerializer):
    doctors = DocterSerializer()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','doctors']

        def update(self,instance,validated_data):
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name',instance.last_name)
            instance.email = validated_data.get('email',instance.email)
            instance.username = validated_data.get('username',instance.username)

            if instance.is_doctor:
                doctor_profile = validated_data.get('doctors')
                if doctor_profile:
                    doctors = Doctors.objects.filter(user = instance)
                    if doctors.exists():
                        doctor = doctors.first()
                        doctor.hospital = doctor_profile.get('hospital',doctor.hospital)
                        doctor.department = doctor_profile.get('department',doctor.department)
                        if doctor.hospital is not None and doctor.department is not None:
                            doctor.is_verified = True
                        doctor.save()
                    else:
                        raise ValidationError("No doctor record found")     
            instance.save()
            return instance
        