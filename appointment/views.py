from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect
from .models import Appointment, TakeAppointment
from .forms import AppointmentForm
from django.contrib import messages
from accounts.decorators import doctor_only,patient_only, oluseg_doctor_only, int_ext_doctors_only, Small_Admin_only, nurse_int_doctors_only
from django.contrib.auth.decorators import login_required
# Create your views here.


#-----------STUDENT---------------APPOINTMENT--------------------------
#new
from datetime import date
today = date.today()

@login_required(login_url='accounts:login')
@patient_only
def quick_appointment(request):
    user_name=request.user.get_username()
    # appointment_list = Appointment.objects.filter(booked=False).order_by("-doctor").order_by("-date")
    appointment_list = Appointment.objects.all().select_related('doctor').filter(booked=False).filter(date__gte=today).order_by("-time_start")
    q=request.GET.get("q")#search start
    if q:
        appointment_list=appointment_list.filter(doctor__first_name__icontains=q)
    else:
        appointment_list = appointment_list# search end

    appointments= {
        "query": appointment_list,
        "user_name":user_name
    }
    return render(request, 'appointment/patient_quick_appointment.html', appointments )


@login_required(login_url='accounts:login')
@patient_only
def patient(request):#this section for my appointment
    user_name=request.user.get_username()#Getting Username as string
    user = request.user  # Getting User as id
    #Getting all Post and Filter By Logged UserName
    appointment_list = TakeAppointment.objects.all().select_related('appointment_with','appointment').order_by("-id").filter(appointment_with=user).select_related('appointment', 'appointment_with')
    q=request.GET.get("q")#search start
    if q:
        appointment_list = appointment_list.filter(appointment__doctor__username__icontains=q).distinct()
    else:
        appointment_list = appointment_list# search end

    appointments= {
        "query": appointment_list,
        "user_name":user_name,
    }
    return render(request, 'appointment/patient.html', appointments )

from notification.models import Notification
from django.core.mail import send_mail
@login_required(login_url='accounts:login')
@patient_only
def appointment_book(request, id):#activate after clicking book now button
    user_name=request.user.get_username()
    user = request.user
    single_appointment= Appointment.objects.get(id=id)
    doc = single_appointment.doctor
    #thank you JESUS
    if not TakeAppointment.objects.filter(appointment_with=request.user).filter(appointment__doctor=single_appointment.doctor).filter(appointment__date=single_appointment.date).exists():
        take = TakeAppointment.objects.create(appointment_id=single_appointment.id)
        take.appointment_with=user
        take.appointment_id = single_appointment.id
        single_appointment.booked = True
        single_appointment.save()
        take.save()
        #return HttpResponseRedirect (instance.get_absolute_url())
        messages.success(request, 'Your Appointment has been scheduled with Dr ' + single_appointment.doctor.username +'.')
        Notification.objects.create(person=doc, message=f'{user.username}  booked an appointment with you!')
        send_mail(
            subject='New Appointment with ' + f'{user_name} ',
            message=f'{user_name} just booked an apapointment with you for ' + f'{single_appointment.date}'+ ' which starts at ' + f'{single_appointment.time_start} ',
            from_email='noreply@olusegun-hospital.com',
            # from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[single_appointment.doctor.email],
        )
    else:
        return HttpResponse('<h1>Errors: You Cannot book two appointment with same doctor on same day </h1>')
        # messages.error(request, 'You Cannot book two appointment with same doctor on same day')
    return redirect('appointment:patient')




#-----------TEACHER---------------APPOINTMENT--------------------------
#new seg
from django.db.models import Q
@login_required(login_url='accounts:login')
@oluseg_doctor_only
def doctor(request):  # this section for my appointment
    user_name = request.user.get_username()
    appointment_list = TakeAppointment.objects.all().select_related('appointment_with','appointment').order_by("-id").filter(appointment__doctor=request.user).select_related('appointment')
    q = request.GET.get("q", '')  # search start
    if q:
        appointment_list = appointment_list.filter(Q(appointment_with__username__icontains=q)| Q(date__icontains=q)).distinct()
    else:
        appointment_list = appointment_list  # search end

    appointments = {
        "query": appointment_list,
        "user_name": user_name
    }
    return render(request, 'appointment/doctor.html', appointments)


from django.http import HttpResponse

@login_required(login_url='accounts:login')
@oluseg_doctor_only
def create_appointment(request):
    user_name = request.user.get_username()  # Getting Username

    # Getting all Post and Filter By Logged UserName
    appointment_list = Appointment.objects.all().select_related('doctor').order_by("-id").filter(doctor=request.user)
    q = request.GET.get("q")  # search start
    if q:
        appointment_list = appointment_list.filter(date__icontains=q)
    else:
        appointment_list = appointment_list  # search end

    form = AppointmentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # similar logic used to verify login - check account - login views
            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']
            date = form.cleaned_data['date']
            if not Appointment.objects.filter(doctor=request.user).filter(date=date).filter(time_end=time_end).filter(time_start=time_start).exists():
                if not Appointment.objects.filter(doctor=request.user).filter(date=date).filter(time_start=time_start).exists() | Appointment.objects.filter(doctor=request.user).filter(date=date).filter(time_end=time_end).exists():
                    new_appointment = form.save(commit=False)
                    new_appointment.doctor = request.user
                    new_appointment.save()
                    messages.success(request, 'APPOINTMENT Created Sucessfully')
                else:
                    messages.error(request, 'Appointment Clashes - Duplicate Start/end times')
            else:
                return HttpResponse('<h1>Errors: Duplicate Entry </h1>')
                # messages.error(request, 'Duplicate Entry - cannot have appointment with several people in same time')
    appointments = {
        "query": appointment_list,
        "user_name": user_name,
        "form": form,
    }
    return render(request, 'appointment/doctor_create_appointment.html', appointments)


@login_required(login_url='accounts:login')
@oluseg_doctor_only
def appointment_delete(request, id):
    single_appointment = Appointment.objects.get(id=id)
    single_appointment.delete()
    messages.success(request, 'Your profile was updated.')
    return redirect('appointment:doctor_appointment_list')


@login_required(login_url='accounts:login')
@oluseg_doctor_only
def doctor_appointment_update(request, id):
    user_name = request.user.get_username()  # Getting Username

    # Getting all Post and Filter By Logged UserName
    appointment_list = Appointment.objects.all().select_related('doctor').order_by("-id").filter(doctor=request.user)

    q = request.GET.get("q")  # search start
    if q:
        appointment_list = appointment_list.filter(date__icontains=q)
    else:
        appointment_list = appointment_list  # search end

    single_appointment = Appointment.objects.get(id=id)
    #new to ensure only the doctor that creates appointment can edit
    if single_appointment.doctor != request.user:
        return HttpResponse('<h1>Errors: You cannot Edit Appointment of another doctor</h1>')
    if single_appointment.booked == True:
        return HttpResponse('Invalid method')
    else:
        form = AppointmentForm(request.POST or None, instance=single_appointment)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.doctor = request.user
            saving.save()
            messages.success(request, 'Post Created Sucessfully')
            return redirect('appointment:doctor_appointment_list')
            #('create_appointment')

    appointments = {
        "query": appointment_list,
        "user_name": user_name,
        "form": form,
    }

    return render(request, 'appointment/doctor_appointment_update.html', appointments)

