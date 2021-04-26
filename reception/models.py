# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.db import models

# project imports
from core.models import TimeStampedModel
from hospital.models import Person, Room, Diagnose
from staff.models import Doctor
import datetime

def increment_patient_number():
  last_patient_id = Patient.objects.all().order_by('id').last()
  if not last_patient_id:
    return 'HOSP' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
  else:
      patient_id = last_patient_id.patient_no
      patient_id_int = int(patient_id[11:14])
      new_booking_int = patient_id_int + 1
      new_patient_id = 'HOSP' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
  return new_patient_id


class Patient(Person):
    patient_no = models.CharField(max_length=25, default=increment_patient_number, editable=False)
    preferred_hospital = models.CharField(max_length=50, blank=True, null=True)
    primary_physician = models.CharField(max_length=50, blank=True, null=True)
    last_physical = models.CharField(max_length=50)
    health_history = models.CharField(max_length=600)
    status = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class In_patient(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_adm = models.DateField(default=timezone.now)
    date_of_discarge = models.DateField()
    diagnosis = models.ForeignKey(Diagnose,  on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    room = models.ForeignKey(Room,  on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.patient, self.room)


class Out_patient(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    diagnosis = models.ForeignKey(Diagnose,  on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.patient)


class MedicalHistory(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    textHistory = models.CharField(max_length=500)

    @property
    def brief_history(self):
        if len(self.textHistory) <= 20:
            return self.textHistory
        else:
            return '{}'.format(truncatechars(self.textHistory, 20))

    def __str__(self):
        return '{}-{}'.format(self.patient, self.brief_history)
