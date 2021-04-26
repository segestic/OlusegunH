from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import IndexView, RoomListView, DiagnoseListView, ElectronicMR, SearchEMR
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path

app_name = 'hospital'

urlpatterns = [
    path('emr/', SearchEMR, name='emr'),
    path('emr/<str:pk>/', ElectronicMR, name='emr'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^room$', views.room_create, name='room_create'),
    url(r'^room/(?P<pk>\d+)/update/$', views.room_update, name='room_update'),
    url(r'^room/(?P<pk>\d+)/delete/$', views.room_delete, name='room_delete'),
    url(r'^rooms$', RoomListView.as_view(), name='rooms'),
    url(r'^diagnose$', views.diagnose_create, name='diagnose_create'),
    url(r'^diagnose/(?P<pk>\d+)/update/$', views.diagnose_update, name='diagnose_update'),
    url(r'^diagnose/(?P<pk>\d+)/delete/$', views.diagnose_delete, name='diagnose_delete'),
    url(r'^diagnoses$', DiagnoseListView.as_view(), name='diagnoses'),
    # path('approve_items/<str:pk>/', views.approve_items, name="approve_items"),
]
