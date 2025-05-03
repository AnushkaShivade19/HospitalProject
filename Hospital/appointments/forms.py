from django import forms
from .models import Appointment
from doctors.models import DoctorProfile

class AppointmentForm(forms.ModelForm):
    specialization = forms.ChoiceField(choices=DoctorProfile.SPECIALIZATION_CHOICES)
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
#from django import forms
from .models import DoctorSchedule

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
class SpecializationFilterForm(forms.Form):
    specialization = forms.ChoiceField(
        choices=DoctorProfile.SPECIALIZATION_CHOICES,
        required=True,
        label='Choose Specialization'
    )
