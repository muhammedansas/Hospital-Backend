from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . serializers import UserRegisterSerializer,MyTokenObtainPairSerializer,UserListSerializer
from . models import User,Doctors

# Create your views here.

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.create_user(
                username = serializer.validated_data['username'],
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
            )
            is_doctor=serializer.validated_data.get("is_doctor",None)
            if is_doctor:
                user.is_doctor=True
                user.save()
                Doctors.objects.create(
                    user=user
                )
            return Response({"message":"Registration Successfully completed"},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_404_NOT_FOUND)
    

class MytokenObtainPairview(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 

class UserProfile(APIView):
    def get(self,request):
        serializer = UserListSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def patch(self,request):
        user = request.user
        data = request.data
        serializer = UserListSerializer(user,data=data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg":"Profile updated"},serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_502_BAD_GATEWAY)
    
    
