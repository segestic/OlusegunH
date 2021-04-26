# from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path

app_name = 'pharmarcy'


urlpatterns = [
    path('create_medicine/', views.create_medicine, name='create_medicine'),
    path('list_medicine/', views.list_medicine, name='list_medicine'),
    path('update_medicine/<str:pk>/', views.update_medicine, name="update_medicine"),
    path('delete_medicine/<str:pk>/', views.delete_medicine, name="delete_medicine"),
    path('create_prescription/', views.create_prescription, name='create_prescription'),
    path('update_prescription/<str:pk>/', views.update_prescription, name="update_prescription"),
    path('list_prescription/', views.list_prescription, name='list_prescription'),
    path('delete_prescription/<str:pk>/', views.delete_prescription, name="delete_prescription"),

]


