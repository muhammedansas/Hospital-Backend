from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . serializers import UserRegisterSerializer,MyTokenObtainPairSerializer
from . models import User

# Create your views here.

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
                is_doctor = serializer.validated_data['is_doctor']
            )
            return Response({"message":"Registration Successfully completed"},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_404_NOT_FOUND)
    

class MytokenObtainPairview(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 