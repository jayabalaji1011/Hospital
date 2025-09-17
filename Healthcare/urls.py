from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/',views.home,name='home'),
    path('staff/',views.staff,name='staff'),
    path('register/', views.register_view, name='register_view'),
    path('staff_register/', views.staff_register, name='staff_register'),
    path('login/', views.login_view, name='login_view'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('userlogout/', views.logout_view, name='logout_view'),
    path('stafflogout/', views.staff_logout, name='staff_logout'),
    path('myappointments/', views.appointment_list, name='appointment_list'),
    path("appointmentrecords",views.appointment_records, name="appointment_records"),
    path("todayappointments",views.today_appointments, name="today_appointments"),
    path('staffaccount/',views.staff_account,name='staff_account'),
    path('useraccount/',views.user_account,name='user_account')
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)