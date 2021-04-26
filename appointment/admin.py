from django.contrib import admin

# Register your models here.

from .models import Appointment, TakeAppointment

class TeacherAdmin(admin.ModelAdmin):
	list_display = ["date", "time_start","time_end","room_number"]
	list_filter = ('date', 'update_time')

class TakeAppointmentAdmin(admin.ModelAdmin):
	list_display = ["date", "appointment_with"]
	list_filter = ('date', 'appointment_with')

admin.site.register(Appointment, TeacherAdmin)

admin.site.register(TakeAppointment, TakeAppointmentAdmin)