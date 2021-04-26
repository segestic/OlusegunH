from django import forms
from .models import Appointment, TakeAppointment

#new for validate
from datetime import date, time, timedelta
from django.core.exceptions import ValidationError
###
#
import datetime
#

def is_future_date_validator(value):
    if value <= date.today():
        raise ValidationError("{0} is not a future date.".format(value))

# def is_future_time_validator(value):
#     if value <= date.today():
#         raise ValidationError("{0} is not a future date.".format(value))



class AppointmentForm(forms.ModelForm):
	date = forms.DateField(validators=[
            is_future_date_validator],widget=forms.DateTimeInput(attrs={'type': 'date'}))
	time_start = forms.TimeField(widget=forms.DateTimeInput(attrs={'type': 'time'}))
	time_end = forms.TimeField(widget=forms.DateTimeInput(attrs={'type': 'time'}))

	# added - because of request.user - i.e to filter the doctor and prevent duplicate doctor record
	# def get_form_kwargs(self):
	# 	kwargs = super(AppointmentForm, self).get_form_kwargs()
	# 	kwargs.update({
	# 		'request': self.request
	# 	})
	# 	return kwargs
	# def get_initial(self):
	# 	init = super(AppointmentForm, self).get_initial()
	# 	init.update({'request': self.request})
	# 	return init


	####end add
	def clean(self):
		super(AppointmentForm, self).clean()
		time_start = self.cleaned_data.get('time_start')
		time_end = self.cleaned_data.get('time_end')
		#new - adding date for filter below
		date = self.cleaned_data.get('date')
		#converting starttime to seconds
		start = str(time_start)
		h, m, s = start.split(':')
		start= (int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds()))
		#endddd

		# converting endtime to seconds
		end = str(time_end)
		h, m, s = end.split(':')
		end = (int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds()))

		diff = end - start
		if diff <= 599: #note 600secs is one minute
			self.add_error('time_end','Appointment duration invalid - min 10mins ahead of start')

########
	# delta = end_date - start_date
	# if delta.days > 0 and (start_date - datetime.date.today()).days >= 0:

###########3
	class Meta:
		model=Appointment
		fields=[
		    "date",
		    "time_start",
		    "time_end",
		    "room_number",
		]









#not useddddddddddddddddd
class TakeAppointmentForm(forms.ModelForm):
	class Meta:
		model = TakeAppointment
		fields = ('appointment_with', 'appointment')

