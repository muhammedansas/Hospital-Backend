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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','profile_image']

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get('first_name',instance.first_name) 
    #     instance.last_name = validated_data.get('last_name',instance.last_name)
    #     instance.username = validated_data.get('username',instance.username)
    #     instance.email = validated_data.get('email',instance.email)
    #     instance.profile_image = validated_data.get('profile_image',instance.profile_image)

    #     instance.save()

    #     return instance

  
class DocterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctors
        fields = ["user","department","hospital","is_verified","image"]
  
    
    def update(self, instance, validated_data):
        # user_data = validated_data.pop('user',None)

        instance.department = validated_data.get('department',instance.department)
        instance.hospital = validated_data.get('hospital',instance.hospital)
        instance.image = validated_data.get('image',instance.image)
        instance.save()

        # if user_data:
        #     user = instance.user
        #     user.username = user_data.get('username',user.username)
        #     user.email = user_data.get('email',user.email)
        #     user.save()

        return instance

# class UserListSerializer(serializers.ModelSerializer):
#     doctors = DocterSerializer()

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','email','doctors',]

#         def update(self,instance,validated_data):
#             instance.first_name = validated_data.get('first_name',instance.first_name)
#             instance.last_name = validated_data.get('last_name',instance.last_name)
#             instance.email = validated_data.get('email',instance.email)
#             instance.username = validated_data.get('username',instance.username)

#             if instance.is_doctor:
#                 doctor_profile = validated_data.get('doctors')
#                 if doctor_profile:
#                     doctors = Doctors.objects.filter(user = instance)
#                     if doctors.exists():
#                         doctor = doctors.first()
#                         doctor.hospital = doctor_profile.get('hospital',doctor.hospital)
#                         doctor.department = doctor_profile.get('department',doctor.department)
#                         if doctor.hospital is not None and doctor.department is not None:
#                             doctor.is_verified = True
#                         doctor.save()
#                     else:
#                         raise ValidationError("No doctor record found")     
#             instance.save()
#             return instance
        