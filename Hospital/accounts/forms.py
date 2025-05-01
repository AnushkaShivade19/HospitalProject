from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Patient

class PatientRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender']
            )
        return user

class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.CharField()
    qualification = forms.CharField()
    experience_years = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                qualification=self.cleaned_data['qualification'],
                experience_years=self.cleaned_data['experience_years']
            )
        return user
