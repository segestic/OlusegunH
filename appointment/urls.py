from django.conf.urls import url
from django.contrib import admin
# from .views import *
from . import views
from django.urls import path

app_name = 'appointment'


urlpatterns=[
    # STUDENT-APPOINTMENT
    path('patient/', views.patient, name='patient'),
    path('my_appointment/', views.patient, name='patient'),
    path('quick_appointment/', views.quick_appointment, name='quick_appointment'),
    path('book/<int:id>/', views.appointment_book, name='appointment_update'),

    #TEACHER-APPOINTMENT
    path('doctorapt/', views.doctor, name='doctor_home'),
    path('my_appointment1/', views.doctor, name='doctor_appointment'),
    path('create_appointment/', views.create_appointment, name='doctor_appointment_list'),
    path('delete1/<int:id>/', views.appointment_delete, name='appointment_delete'),
    path('update1/<int:id>/', views.doctor_appointment_update, name='doctor_appointment_update'),
]
