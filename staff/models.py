# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.models import User, Doctor
from django.db import models

from core.models import TimeStampedModel
from hospital.models import Person


# Create your models here.
class UserType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Type'
        verbose_name_plural = 'User Types'


def get_doctors():
    doctor =  UserType.objects.get_or_create(name='Doctors', description='Doctors')
    return doctor.id

def get_nurses():
    nurse = UserType.objects.get_or_create(name='Nurses', description='Nurses')
    return nurse.id


class Speciality(models.Model):
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'


class Doctor(models.Model):
    person = models.OneToOneField(Doctor, related_name='doctors', on_delete=models.CASCADE)
    specialty = models.ManyToManyField('Speciality')
    designation = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{}'.format(self.person)


class Nurse(models.Model):
    person = models.OneToOneField(User, related_name='nurses', on_delete=models.CASCADE)
    specialty = models.ManyToManyField('Speciality')
    designation = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{}'.format(self.person)


class OtherStaff(Person):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ManyToManyField('Speciality')
    designation = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

