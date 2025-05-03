from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'diagnosis', 'medications', 'notes', 'prescription_file']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control'}),
            'medications': forms.Textarea(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }
