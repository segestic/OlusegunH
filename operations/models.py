# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.timezone import now

# from django.utils.timezone.now import timezone
from django.utils import timezone

from core.models import TimeStampedModel
from reception.models import Patient
from hospital.models import Diagnose
from staff.models import Doctor, Nurse


class Treatment(TimeStampedModel):
    date = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.ForeignKey(Diagnose,  on_delete=models.CASCADE)
    doctors_comments = models.TextField()

    def __str__(self):
        return 'Treated for -{}'.format(self.diagnosis)
        # return '{}-{}'.format(self.patient, self.diagnosis)



class Vaccine(TimeStampedModel):
    name = models.CharField(max_length=100)
    live = models.BooleanField(null=True)
    absorved = models.BooleanField(null=True)
    inactivated = models.BooleanField(null=True)
    oral = models.BooleanField(null=True)

    def __str__(self):
        return self.name

class VaccineApplied(TimeStampedModel):
    date = models.DateField(default=timezone.now)
    vaccine = models.ForeignKey(Vaccine,  on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,  on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)

    def __str__(self):
        return '%s | by  %s (%s)' % (self.patient, self.nurse, self.date)

    class Meta:
        verbose_name = 'Vaccine Applied'
        verbose_name_plural = 'Vaccines usage'


class Test(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MedicalTest(TimeStampedModel):
    date = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient,  on_delete=models.CASCADE)
    test = models.ForeignKey(Test,  on_delete=models.CASCADE)
    results = models.CharField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.patient, self.test.name)
