# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django imports
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse

# project imports
from .models import Diagnose, Room
from .forms import DiagnoseForm, RoomForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import doctor_only,patient_only, oluseg_doctor_only, int_ext_doctors_only, Small_Admin_only, nurse_int_doctors_only

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'hospital/index.html'

#seg19.3
from finance.models import Billing
from pharmarcy.models import Prescription
from reception.models import Patient
from operations.models import VaccineApplied, MedicalTest, Treatment

# class SegView(LoginRequiredMixin, DetailView):
#     template_name = 'hospital/specific.html'


    # def get(self, request, pk):
    #     patient_id = pk
    #     try:
    #         q1 = Billing.objects.filter(patient=patient_id)
    #         q2 = Prescription.objects.all(user=patient_id).select_related('doctor')
    #         q3 = Treatment.objects.filter(patient=patient_id).select_related('doctor')
    #         q4 = VaccineApplied.objects.filter (patient=patient_id)
    #         q5 = MedicalTest.objects.filter (patient=patient_id)
    #     except :
    #         pass
    #     context = {}
    #     context['billing'] = q1
    #     context['prescriptions'] = q2
    #     context ['treatment'] = q3
    #     context['VaccineApplied'] = q4
    #     context['MedicalTest'] = q5
    #     return render(request, self.template_name, context)
from django.db.models import Q
#.filter(Q(appointment_with__username__icontains=q)| Q(date__icontains=q)).distinct()

@login_required
@int_ext_doctors_only
def SearchEMR(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Patient.objects.filter(Q(dob__iexact=query)| Q(patient_no__iexact=query)).distinct()

    context = {'query': query,
               'results': results}

    return render(request, 'hospital/searchemr.html', context)

@login_required
@int_ext_doctors_only
def ElectronicMR(request, pk):
    patient = Patient.objects.get(id=pk)
    try:
        # q1 = Billing.objects.filter(patient_id=pk).select_related('treatment')
        q2 = Prescription.objects.filter(patient_id=patient).select_related('doctor','patient','drug')
        q3 = Treatment.objects.filter(patient_id=patient).select_related('doctor','patient','diagnosis')
        q4 = VaccineApplied.objects.filter(patient_id=patient).select_related('vaccine','patient','nurse')
        q5 = MedicalTest.objects.filter(patient_id=patient).select_related('patient','test')
    except:
        pass
    context = {}
    context['patient'] = patient
    # context['billing'] = q1
    context['prescriptions'] = q2
    context['treatment'] = q3
    context['VaccineApplied'] = q4
    context['MedicalTest'] = q5
    return render(request, 'hospital/specific.html', context)




# create fbv for a diagnose modal form for create, update and delete

def save_diagnose_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            diagnoses = Diagnose.objects.all()
            data['html_diagnose_list'] = render_to_string("hospital/includes/partial_diagnose_list.html",
                {'diagnoses': diagnoses}
            )
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@oluseg_doctor_only
def diagnose_create(request):
    if request.method == 'POST':
        form = DiagnoseForm(request.POST)
    else:
        form = DiagnoseForm()
    return save_diagnose_form(request, form, 'hospital/diagnose_form.html')


@login_required
@oluseg_doctor_only
def diagnose_update(request, pk):
    diagnose = get_object_or_404(Diagnose, pk=pk)
    if request.method == 'POST':
        form = DiagnoseForm(request.POST, instance=diagnose)
    else:
        form = DiagnoseForm(instance=diagnose)
    return save_diagnose_form(request, form, 'hospital/diagnose_update.html')

@login_required
@Small_Admin_only
def diagnose_delete(request, pk):
    diagnose = get_object_or_404(Diagnose, pk=pk)
    data = dict()
    if request.method == 'POST':
        diagnose.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        diagnoses = Diagnose.objects.all()
        data['html_diagnose_list'] = render_to_string('hospital/includes/partial_diagnose_list.html',
            {'diagnoses': diagnoses}
        )
    else:
        context = {'diagnose': diagnose}
        data['html_form'] = render_to_string('hospital/diagnose_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

# create fbv for a room modal form for create, update and delete
def save_room_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            rooms = Room.objects.all().select_related('room_type','departmnt').order_by('room_number')
            data['html_room_list'] = render_to_string('hospital/includes/partial_room_list.html',
                {'rooms': rooms}
            )
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
@nurse_int_doctors_only
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
    else:
        form = RoomForm()
    return save_room_form(request, form, 'hospital/room_form.html')

@login_required
@nurse_int_doctors_only
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
    else:
        form = RoomForm(instance=room)
    return save_room_form(request, form, 'hospital/room_update.html')


@login_required
@Small_Admin_only
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    data = dict()
    if request.method == 'POST':
        room.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        rooms = Room.objects.all().select_related('room_type','departmnt').order_by('room_number')
        data['html_room_list'] = render_to_string('hospital/includes/partial_room_list.html',
            {'rooms': rooms}
        )
    else:
        context = {'room': room}
        data['html_form'] = render_to_string('hospital/room_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)




# cbv listviews for oluseg app
@method_decorator([login_required, oluseg_doctor_only], name ='dispatch')
class DiagnoseListView(ListView):
    context_object_name = 'diagnoses'
    model = Diagnose
    template_name = 'hospital/diagnose_list.html'

    def get_queryset(self):
        return Diagnose.objects.all()


@method_decorator([login_required, nurse_int_doctors_only], name ='dispatch')
class RoomListView(ListView):
    context_object_name = 'rooms'
    model = Room
    template_name = 'hospital/room_list.html'

    def get_queryset(self):
        return Room.objects.all().order_by('room_number')
