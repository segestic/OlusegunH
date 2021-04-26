from django import forms
from staff.models import Doctor

# crispy_forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiWidgetField, Submit

class DoctorForm(forms.ModelForm):
    # TODO: Define other fields here

    class Meta:
        model = Doctor
        fields = ['person']

        labels = {
            'person': 'Int/Ext Doctor'
        }


    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_tag = False

        self.helper.layout = Layout(
             'person',
            )


    def clean(self):
        cleaned_data = super(DoctorForm, self).clean()
        return cleaned_data
