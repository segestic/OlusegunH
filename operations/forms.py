from django import forms
from operations.models import Treatment, Vaccine, VaccineApplied, Test, MedicalTest

# crispy_forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiWidgetField, Submit

class TreatmentForm(forms.ModelForm):
    # TODO: Define other fields here

    class Meta:
        model = Treatment
        fields = ['patient', 'date', 'symptoms', 'diagnosis', 'doctors_comments']

        labels = {
            'doctors_comments': "Doctor's Comments"
            }

        widgets = {
            'date': forms.SelectDateWidget(years=[str(val) for val in range(1998, 2021)]),
            'symptoms': forms.Textarea(attrs={'rows':4, 'style':'resize:none;'}),
            'doctors_comments': forms.Textarea(attrs={'rows':4, 'style':'resize:none;'}),
            }

    def __init__(self, *args, **kwargs):
        super(TreatmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields['symptoms'].widget.attrs['style'] = 'resize:none' //setting textarea resize to none
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'patient',
            'doctor',
            MultiWidgetField(
                'date',
                attrs=(
                    {'style': 'width: 32.8%; display: inline-block;'}
                )
            ),
            'symptoms',
            'diagnosis',
            'doctors_comments',
        )


    def clean(self):
        cleaned_data = super(TreatmentForm, self).clean()
        return cleaned_data

class VaccineCreateForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = '__all__'

class VaccineUpdateForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = '__all__'

class VaccineAppliedCreateForm(forms.ModelForm):
    class Meta:
        model = VaccineApplied
        fields = ['vaccine', 'patient', 'nurse']

class VaccineAppliedUpdateForm(forms.ModelForm):
    class Meta:
        model = VaccineApplied
        fields = ['vaccine', 'patient', 'nurse']

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

class TestUpdateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

class MedicalTestCreateForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = MedicalTest
        fields = ['patient', 'test', 'results', 'status']

class MedicalTestUpdateForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = MedicalTest
        fields = ['patient', 'test', 'results']