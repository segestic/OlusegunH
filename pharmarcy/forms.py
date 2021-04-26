from django import forms
from .models import Medicine, Prescription


class MedicineCreateForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class MedicineUpdateForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class PrescriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'drug', 'description', 'dosage', 'quantity', 'instructions']

class PrescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        # fields = ['vaccine', 'patient', 'nurse']