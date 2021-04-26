# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from .forms import TreatmentForm
from .models import Treatment, VaccineApplied, Test, MedicalTest
from staff.models import Doctor
from accounts.decorators import doctor_only,patient_only, oluseg_doctor_only, int_ext_doctors_only, Small_Admin_only, nurse_int_doctors_only
from django.contrib.auth.decorators import login_required

# create fbv for a treatment modal form for create, update and delete

@login_required
@oluseg_doctor_only
def save_treatment_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            temp = form.save(commit=False)
            doc = Doctor.objects.get(person_id=request.user.id)
            temp.doctor_id = doc.id
            temp.save()
            data['form_is_valid'] = True
            treatments = Treatment.objects.all()
            data['html_treatment_list'] = render_to_string("operations/includes/partial_treatment_list.html",
                {'treatments': treatments}
            )
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@oluseg_doctor_only
def treatment_create(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
    else:
        form = TreatmentForm()
    return save_treatment_form(request, form, 'operations/treatment_form.html')


@login_required
@oluseg_doctor_only
def treatment_update(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
    else:
        form = TreatmentForm(instance=treatment)
    return save_treatment_form(request, form, 'operations/treatment_update.html')


@login_required
@Small_Admin_only
def treatment_delete(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    data = dict()
    if request.method == 'POST':
        treatment.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        treatments = Treatment.objects.all()
        data['html_treatment_list'] = render_to_string('operations/includes/partial_treatment_list.html',
            {'treatments': treatments}
        )
    else:
        context = {'treatment': treatment}
        data['html_form'] = render_to_string('operations/treatment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


@method_decorator ([login_required, oluseg_doctor_only], name ='dispatch')
class TreatmentListView(ListView):
    context_object_name = 'treatments'
    model = Treatment
    template_name = 'operations/treatment_list.html'

    def get_queryset(self):
        #seg add select_related. from 12 to 3 queries
        return Treatment.objects.all().select_related('diagnosis', 'patient', 'doctor')


#############CRUD
from .models import Vaccine
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VaccineCreateForm, VaccineUpdateForm, VaccineAppliedCreateForm, VaccineAppliedUpdateForm, TestCreateForm, TestUpdateForm, MedicalTestCreateForm, MedicalTestUpdateForm
from notification.models import Notification
#create

@login_required
@nurse_int_doctors_only
def create_vaccine(request):
    # if request.session.has_key('username'):
    user = request.user
    form = VaccineCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        Notification.objects.create(person=user, message=f'{user.username} added a new vaccine!')
        return redirect('operations:list_vaccine')
    context = {
        "form": form,
        "title": "Add Vaccine",
    }
    return render(request, "operations/vaccine_form.html", context)

#Read#
@login_required
@nurse_int_doctors_only
def list_vaccine(request):
    title = 'List of Vaccines'
    #logic to display form as modal
    form = VaccineCreateForm(request.POST or None)
    queryset = Vaccine.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "operations/vaccine_list.html", context)

#Update Vaccine
@login_required
@nurse_int_doctors_only
def update_vaccine(request, pk):
    queryset = Vaccine.objects.get(id=pk)
    form = VaccineUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = VaccineUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('operations:list_vaccine')
    context = {
        'form': form
    }
    return render(request, 'operations/vaccine_update.html', context)


#Delete
@login_required
@nurse_int_doctors_only
def delete_vaccine(request, pk):
    queryset = Vaccine.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('operations:list_vaccine')
    context = {
        'vaccine': queryset
    }
    return render(request, 'operations/vaccine_delete.html', context)

#-------------==---------------------------

#create
@login_required
@Small_Admin_only
def applied_vaccine(request):
    # if request.session.has_key('username'):
    form = VaccineAppliedCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('operations:list_applied_vaccine')
    context = {
        "form": form,
        "title": "Apply Vaccine",
    }
    return render(request, "operations/vaccine_applied_form.html", context)

#Read#
@login_required
@nurse_int_doctors_only
def list_applied_vaccine(request):
    title = 'List of Vaccines Applied'
    #logic to display form as modal
    form = VaccineAppliedCreateForm(request.POST or None)
    queryset = VaccineApplied.objects.all().select_related('vaccine','patient','nurse')
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "operations/vaccine_applied_list.html", context)

#Update Vaccine
@login_required
@Small_Admin_only
def update_applied_vaccine(request, pk):
    queryset = VaccineApplied.objects.get(id=pk)
    form = VaccineAppliedUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = VaccineAppliedUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('operations:list_applied_vaccine')
    context = {
        'form': form
    }
    return render(request, 'operations/vaccine_applied_update.html', context)


#Delete
@login_required
@Small_Admin_only
def delete_applied_vaccine(request, pk):
    queryset = VaccineApplied.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('operations:list_applied_vaccine')
    context = {
        'vaccine': queryset
    }
    return render(request, 'operations/vaccine_applied_delete.html', context)


#TESTTTTTTTTTTTT
#create
@login_required
@nurse_int_doctors_only
def create_test(request):
    # if request.session.has_key('username'):
    form = TestCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('operations:list_test')
    context = {
        "form": form,
        "title": "Add Test",
    }
    return render(request, "operations/test_form.html", context)

#Read#
@login_required
@nurse_int_doctors_only
def list_test(request):
    title = 'List of Patients Test'
    #logic to display form as modal
    form = TestCreateForm(request.POST or None)
    queryset = Test.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "operations/test_list.html", context)

#Update Vaccine
@login_required
@Small_Admin_only
def update_test(request, pk):
    queryset = Test.objects.get(id=pk)
    form = TestUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = TestUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('operations:list_test')
    context = {
        'form': form
    }
    return render(request, 'operations/test_update.html', context)


#Delete
@login_required
@nurse_int_doctors_only
def delete_test(request, pk):
    queryset = Test.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('operations:list_test')
    context = {
        'test': queryset
    }
    return render(request, 'operations/test_delete.html', context)

#-------------==---------------------------
#-------------------------------------Medical Test---------------------------

#create
@login_required
@nurse_int_doctors_only
def create_medical_test(request):
    # if request.session.has_key('username'):
    form = MedicalTestCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('operations:list_medical_test')
    context = {
        "form": form,
        "title": "Add Medical Test",
    }
    return render(request, "operations/medical_test_form.html", context)

#Read#
@nurse_int_doctors_only
@oluseg_doctor_only
def list_medical_test(request):
    title = 'List of Medical Test(s)'
    #logic to display form as modal
    form = MedicalTestCreateForm(request.POST or None)
    queryset = MedicalTest.objects.all().select_related('patient','test')
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "operations/medical_test_list.html", context)

#Update Vaccine
@login_required
@Small_Admin_only
def update_medical_test(request, pk):
    queryset = MedicalTest.objects.get(id=pk)
    form = MedicalTestUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = MedicalTestUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('operations:list_medical_test')
    context = {
        'form': form
    }
    return render(request, 'operations/medical_test_update.html', context)


#Delete
@login_required
@Small_Admin_only
def delete_medical_test(request, pk):
    queryset = MedicalTest.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('operations:list_medical_test')
    context = {
        'test': queryset
    }
    return render(request, 'operations/medical_test_delete.html', context)