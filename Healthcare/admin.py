from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'phone', 'gender', 'specialist', 'appointment_date', 'time_slot', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone', 'specialist')
    list_filter = ('gender', 'specialist', 'appointment_date', 'time_slot')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile')
    search_fields = ('name', 'mobile')

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile')
    search_fields = ('name', 'mobile')
    
    