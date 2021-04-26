from django.conf.urls import url
from django.contrib import admin
from .views import TreatmentListView
from . import views
from django.urls import path

app_name = 'operations'

urlpatterns = [
    url(r'^treatment$', views.treatment_create, name='treatment_create'),
    url(r'^treatment/(?P<pk>\d+)/update/$', views.treatment_update, name='treatment_update'),
    url(r'^treatment/(?P<pk>\d+)/delete/$', views.treatment_delete, name='treatment_delete'),
    url(r'^treatments$', TreatmentListView.as_view(), name='treatments'),
    path('create_vaccine/', views.create_vaccine, name='create_vaccine'),
    path('list_vaccine/', views.list_vaccine, name='list_vaccine'),
    path('update_applied_vaccine/<str:pk>/', views.update_applied_vaccine, name="update_applied_vaccine"),
    path('update_vaccine/<str:pk>/', views.update_vaccine, name="update_vaccine"),
    path('delete_vaccine/<str:pk>/', views.delete_vaccine, name="delete_vaccine"),
    path('applied_vaccine/', views.applied_vaccine, name='applied_vaccine'),
    path('list_applied_vaccine/', views.list_applied_vaccine, name='list_applied_vaccine'),
    path('delete_applied_vaccine/<str:pk>/', views.delete_applied_vaccine, name="delete_applied_vaccine"),
    path('create_test/', views.create_test, name='create_test'),
    path('list_test/', views.list_test, name='list_test'),
    path('update_test/<str:pk>/', views.update_test, name="update_test"),
    path('delete_test/<str:pk>/', views.delete_test, name="delete_test"),
    path('create_medical_test/', views.create_medical_test, name='create_medical_test'),
    path('list_medical_test/', views.list_medical_test, name='list_medical_test'),
    path('update_medical_test/<str:pk>/', views.update_medical_test, name="update_medical_test"),
    path('delete_medical_test/<str:pk>/', views.delete_medical_test, name="delete_medical_test"),

]


