# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from core.models import TimeStampedModel
from reception.models import Patient
from staff.models import Doctor

# project imports
class Medicine(TimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.IntegerField(default=0, unique=True)
    description = models.TextField()
    supplier = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Prescription(TimeStampedModel):
    doctor = models.ForeignKey(Doctor, related_name='prescribing_doctors',  on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name='prescribed_patients',  on_delete=models.CASCADE)
    drug = models.ForeignKey(Medicine, related_name='prescribed_drugs',  on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    dosage = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    instructions = models.CharField(max_length=500)

    @property
    def charges(self):
        pass

    def __str__(self):
        return '{}-{}-{}'.format(self.doctor, self.patient, self.drug)
