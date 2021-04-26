# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse_lazy
#old - depreciated
# from django.views.generic import CreateView, ListView
#newseg
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Patient, In_patient, Out_patient, Diagnose
from .forms import PatientForm, In_patientForm, Out_patientForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from accounts.decorators import nurse_only,patient_only, oluseg_doctor_only, int_ext_doctors_only, Small_Admin_only, nurse_int_doctors_only
from django.contrib.auth.decorators import login_required

# Create your views here.
# class PatientCreateView(SuccessMessageMixin, CreateView):
#     model = Patient
#     form_class = PatientForm
#     template_name = 'reception/patient_form.html'
#     success_url = reverse_lazy('reception:patients')
#     success_message = 'Patient records entered successfully'

    # def get_success_url(self):
    #     # return reverse_lazy('reception:patients')
    #     return reverse_lazy('/')

@login_required
@nurse_only
def PatientCreateView(request):
    # if request.session.has_key('username'):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('reception:patients')
    context = {
        "form": form,
    }
    return render(request, "reception/patient_form.html", context)


# def form_valid(self, form):
#     form.save()
#     # return super().form_valid(form)
#     return redirect(self.get_success_url())

@method_decorator ([login_required, nurse_only], name ='dispatch')
class In_patientCreateView(SuccessMessageMixin, CreateView):
    model = In_patient
    template_name = 'reception/in_patient_form.html'
    form_class = In_patientForm
    success_message = 'In-Patient records entered successfully'

    def get_success_url(self):
        return reverse_lazy('reception:patients')

@method_decorator ([login_required, nurse_only], name ='dispatch')
class Out_patientCreateView(SuccessMessageMixin, CreateView):
    model = Out_patient
    template_name = 'reception/out_patient_form.html'
    form_class = Out_patientForm
    success_message = 'Out-Patient records entered successfully'

    def get_success_url(self):
        return reverse_lazy('reception:patients')

@method_decorator ([login_required, nurse_int_doctors_only], name ='dispatch')
class PatientListView(ListView):
    context_object_name = 'patient_list'
    model = Patient
    template_name = 'reception/reception_list.html'

    def get_queryset(self):
        return Patient.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['in_patient_list'] = In_patient.objects.all().select_related('diagnosis','patient','room','doctor')
        context['out_patient_list'] = Out_patient.objects.all().select_related('diagnosis','patient')
        return context


@method_decorator ([login_required, nurse_int_doctors_only], name ='dispatch')
class In_patientListView(ListView):
    context_object_name = 'in_patient_list'
    model = In_patient
    template_name = 'reception/reception_list.html'

    def get_queryset(self):
        return In_patient.objects.all().select_related('diagnosis','patient','room','doctor')


@method_decorator ([login_required, nurse_int_doctors_only], name ='dispatch')
class Out_patientListView(ListView):
    context_object_name = 'out_patient_list'
    model = Out_patient
    template_name = 'reception/reception_list.html'

    def get_queryset(self):
        return Out_patient.objects.all().select_related('diagnosis','patient')
