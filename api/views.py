from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from . serializers import UserRegisterSerializer,MyTokenObtainPairSerializer,UserSerializer,DoctorSerializer
from . models import User,Doctors

# Create your views here.

class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        print(request.data,"tyuio")
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
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class MytokenObtainPairview(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 


class UsersList(APIView):
    def get(self,request):
        obj = User.objects.all()
        serializer = UserSerializer(obj,many=True)
        return Response(serializer.data)
    

class DoctorList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        obj = Doctors.objects.all()
        serializer = DoctorSerializer(obj,many=True)
        return Response(serializer.data)
    
    def patch(self,request):
        user = request.user
        data = request.data
        serializer = UserSerializer(user,data=data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Msg":"Profile updated"},serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_502_BAD_GATEWAY)
    
class DoctorProfile(APIView):
    def get(self, request):
        print("get works")
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            obj = Doctors.objects.get(user=user)
            print(obj.department)
            serializer = DoctorSerializer(obj)
            return Response(serializer.data)
        except Doctors.DoesNotExist:
            return Response({"detail": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
       
        doctor_data = Doctors.objects.get(user = request.user)
        serializer = DoctorSerializer(doctor_data, data=request.data, partial=True)
        print("patch works")
        print(request.data)
        if serializer.is_valid():
           
            print(serializer.validated_data,'././././')
            serializer.save()
            
            return Response({"Msg": "Profile updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    def get(self, request):
        try:
            obj = User.objects.get(email=request.user)
            serializer = UserSerializer(obj)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"detail": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        user_data = User.objects.get(email = request.user)
        serializer = UserSerializer(user_data, data=request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data,'././././')
            serializer.save()
            return Response({"Msg": "Profile updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)