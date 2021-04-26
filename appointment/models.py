# -*- coding: utf-8 -*-
from core.models import TimeStampedModel
# from reception.models import Patient

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Appointment(models.Model):
    doctor = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='apt_doctors')
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    room_number = models.CharField(max_length=50)
    booked = models.BooleanField(default=False)
    update_time = models.DateField(auto_now=True, auto_now_add=False)
    frist_time = models.DateField(auto_now=False, auto_now_add=True)

    # show filed in admin panel
    def __str__(self):
        return self.date

    def __str__(self):
        return self.time_start

    def __str__(self):
        return self.time_end

    def __str__(self):
        return self.room_number


from django.utils import timezone

class TakeAppointment(models.Model):
    appointment_with = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='apt_patients')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.appointment + 'Appointment Booked'


