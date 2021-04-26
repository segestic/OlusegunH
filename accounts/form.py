from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Patient, Doctor

PATIENT = 1
EXT_DOCTOR = 2
NURSE = 3
INT_DOCTOR = 4
LAB_OFFICER = 5
SMALLADMIN = 6

BLOOD_GROUPS = (
    ('0 Rh-', '0 Rh-'),
    ('0 Rh+', '0 Rh+'),
    ('A Rh-', 'A Rh-'),
    ('A Rh+', 'A Rh+'),
    ('B Rh-', 'B Rh-'),
    ('B Rh+', 'B Rh+'),
    ('AB Rh-', 'AB Rh-'),
    ('AB Rh+', 'AB Rh+'),
)


# user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)

class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email address already in use.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        # adding * below to getting all data in list.
        role = self.cleaned_data.get(*['roles'])
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        # first save the initial data
        user.user_type = 1
        # user.save()
        # loop through the list and add it to roles - u can use get or create
        # if you use get, you would need to add roles in admin section - that is better i think.
        # for x in role:
        #     a2 = Role.objects.get(id=x)
        #     user.roles.add(a2)
        user.save()
        patient = Patient.objects.create(user=user)
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.location = self.cleaned_data.get('location')
        patient.blood_group = self.cleaned_data.get('blood_group')
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    department = (
        ('Dentistry', "Dentistry"),
        ('Cardiology', "Cardiology"),
        ('ENT Specialists', "ENT Specialists"),
        ('Astrology', 'Astrology'),
        ('Neuroanatomy', 'Neuroanatomy'),
        ('Blood Screening', 'Blood Screening'),
        ('Eye Care', 'Eye Care'),
        ('Physical Therapy', 'Physical Therapy'),
    )

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    identification_number = forms.CharField(required=True)
    department = forms.ChoiceField(choices=department)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_identification_number(self):
        identification_number = self.cleaned_data.get('identification_number')
        if Doctor.objects.filter(identification_number=identification_number).exists():
            raise forms.ValidationError('Identification Number already in use.')
        return identification_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith(('@olusegun.com', '@doctor.com', '@hospitalmail.com')):
            raise forms.ValidationError('Invalid Email')
        elif User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email address already in use.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        # new add seg; user.is_active = False
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.user_type = 2
        # a2 = Role.objects.get(id=2)
        # a2 = Role.objects.get_or_create(id=2)
        # user.roles.add(a2)
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number = self.cleaned_data.get('phone_number')
        doctor.identification_number = self.cleaned_data.get('identification_number')
        doctor.department = self.cleaned_data.get('department')
        doctor.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']


class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone_number', 'location', 'blood_group']


class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['phone_number', 'department']