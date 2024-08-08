from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',views.UserRegistration.as_view(),name='register'),
    path('login/',views.MytokenObtainPairview.as_view(),name='login'),
    path('Userprofile/',views.UserProfile.as_view(),name='Userprofile'),
    path('Userlist/',views.UsersList.as_view(),name='userlist'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('doctorsList/',views.DoctorList.as_view(),name='doctorsList'),
    path('doctorProfile/',views.DoctorProfile.as_view(),name='doctorProfile'),
]
