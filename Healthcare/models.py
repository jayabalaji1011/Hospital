from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import time,timedelta,datetime
import datetime 
import os
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def getFilename(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)


# Patient Model
class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256)  # hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} - {self.mobile}"



# Staff/Admin Model
class StaffUser(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256)  # hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} - {self.mobile}"



class Appointment(models.Model):
    patient = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey('StaffUser', on_delete=models.SET_NULL, null=True, blank=True)

    # Patient Info
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female'), ('Other','Other')])

    # Doctor Choices
    DOCTOR_CHOICES = [
        ('cardiologist', 'Cardiologist'),
        ('gastroenterologist', 'Gastroenterologist'),
        ('orthopedic', 'Orthopedic Surgeon'),
        ('general_physician', 'General Physician'),
        ('neurologist', 'Neurologist'),
        ('dermatologist', 'Dermatologist'),
    ]
    specialist = models.CharField(max_length=50, choices=DOCTOR_CHOICES)

    # Appointment date & slot
    appointment_date = models.DateField(default=timezone.now)
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (9 AM - 12 PM)'),
        ('afternoon', 'Afternoon (1:30 PM - 4 PM)'),
        ('evening', 'Evening (6 PM - 9 PM)'),
    ]
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='morning')

    # Exact consultation time
    consultation_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('visited', 'Visited'),
        ('not_visited', 'Not Visited'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} - {self.specialist} on {self.appointment_date} ({self.time_slot})"

    # Map specialist to consultation duration in minutes
    @staticmethod
    def consultation_time_map():
        return {
            'general_physician': 15,
            'cardiologist': 30,
            'neurologist': 45,
            'gastroenterologist': 20,
            'orthopedic': 20,
            'dermatologist': 15,
        }

    # Map slot to start & end time
    @staticmethod
    def slot_timings():
        return {
            'morning': (time(9, 0), time(12, 0)),
            'afternoon': (time(13, 30), time(16, 0)),
            'evening': (time(18, 0), time(21, 0)),
        }


