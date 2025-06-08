from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Patient
from doctors.models import DoctorProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
    # User fields
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    # Doctor profile fields
    specialization = forms.ChoiceField(choices=DoctorProfile.SPECIALIZATION_CHOICES)
    qualification = forms.CharField(max_length=200)
    years_of_experience = forms.IntegerField()
    clinic_address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    available_for_online = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Ensure required keys exist
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data.get('specialization', ''),
                qualification=self.cleaned_data.get('qualification', ''),
                years_of_experience=self.cleaned_data.get('years_of_experience', 0),
                clinic_address=self.cleaned_data.get('clinic_address', ''),
                phone_number=self.cleaned_data.get('phone_number', ''),
                profile_picture=self.cleaned_data.get('profile_picture', None),
                bio=self.cleaned_data.get('bio', ''),
                available_for_online=self.cleaned_data.get('available_for_online', False)
            )

        return user