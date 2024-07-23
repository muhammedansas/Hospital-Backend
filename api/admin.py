from django.contrib import admin
from . models import  User,Doctors

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_doctor']

@admin.register(Doctors)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','user','hospital','department')