from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
# seg
from .import views
from django.urls import path
# seg

app_name = 'accounts'



urlpatterns=[
     path('register/',views.register, name='register'),
     path('patient_register/',views.patient_register.as_view(), name='patient_register'),
     path('doctor_register/',views.doctor_register.as_view(), name='doctor_register'),
     path('login/',views.login_request, name='login'),
     #login scam
     path('logout/',views.logout_view, name='logout'),
     #profile for patient i.e non-staff
     path('profile/', views.patient_profile, name='user-profile'),
     path('profile/update/', views.profile_update, name='user-profile-update'),
     #new #profile for doctor/staff
     path('profile2/', views.doctor_profile, name='doctor-profile'),
     path('profile2/update/', views.doctor_profile_update, name='doctor-profile-update'),
     #for activation
     path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
     #new add for 2nd type user activate
     path('activate2/<uidb64>/<token>/', views.ActivateAccountDoctor.as_view(), name='activate2'),
     #path just to render confirm - new seg
     path('confirme/', views.confirm, name='confirm'),
]

