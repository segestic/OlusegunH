# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

#############CRUD
from .models import Medicine, Prescription
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.utils.decorators import method_decorator
from accounts.decorators import doctor_only,patient_only, oluseg_doctor_only, int_ext_doctors_only, Small_Admin_only, nurse_int_doctors_only
from django.contrib.auth.decorators import login_required
from staff.models import Doctor

#create
@login_required
@nurse_int_doctors_only
def create_medicine(request):
    # if request.session.has_key('username'):
    form = MedicineCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('pharmarcy:list_medicine')
    context = {
        "form": form,
        "title": "Add Medcine",
    }
    return render(request, "pharmarcy/medcine_form.html", context)

#Read#
@login_required
@nurse_int_doctors_only
def list_medicine(request):
    title = 'List of Medicine'
    #logic to display form as modal
    form = MedicineCreateForm(request.POST or None)
    queryset = Medicine.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "pharmarcy/medicine_list.html", context)

#Update Vaccine
@login_required
@nurse_int_doctors_only
def update_medicine(request, pk):
    queryset = Medicine.objects.get(id=pk)
    form = MedicineUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = MedicineUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('pharmarcy:list_medicine')
    context = {
        'form': form
    }
    return render(request, 'pharmarcy/medicine_update.html', context)


#Delete
@login_required
@nurse_int_doctors_only
def delete_medicine(request, pk):
    queryset = Medicine.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('pharmarcy:list_medicine')
    context = {
        'medicine': queryset
    }
    return render(request, 'pharmarcy/medicine_delete.html', context)

#-------------==-------------------------------









#create


@login_required
@oluseg_doctor_only
def create_prescription(request):
    # if request.session.has_key('username'):
    form = PrescriptionCreateForm(request.POST or None)
    if form.is_valid():
        # j=User.objects.get(id=request.user.id)
        doc = Doctor.objects.get(person_id=request.user.id)
        prescription = form.save(commit=False)
        prescription.doctor_id = doc.id
        prescription.save()
        messages.success(request, 'Successfully Created')
        return redirect('pharmarcy:list_prescription')
    context = {
        "form": form,
        "title": "Add Prescription",
    }
    return render(request, "pharmarcy/prescription_form.html", context)

#Read#
@login_required
@oluseg_doctor_only
def list_prescription(request):
    title = 'List of Medicine'
    #logic to display form as modal
    form = PrescriptionCreateForm(request.POST or None)
    queryset = Prescription.objects.all().select_related('doctor','patient','drug')
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    return render(request, "pharmarcy/prescription_list.html", context)

# #Update Vaccine
@oluseg_doctor_only
@oluseg_doctor_only
def update_prescription(request, pk):
    queryset = Medicine.objects.get(id=pk)
    form = PrescriptionUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = PrescriptionUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('pharmarcy:medcine_list')
    context = {
        'form': form
    }
    return render(request, 'pharmarcy/prescription_update.html', context)


# Delete
@login_required
@Small_Admin_only
def delete_prescription(request, pk):
    queryset = Prescription.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('pharmarcy:list_medicine')
    context = {
        'prescription': queryset
    }
    return render(request, 'pharmarcy/prescription_delete.html', context)

#-------------==-