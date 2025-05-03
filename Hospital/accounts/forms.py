from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Patient
from doctors.models import DoctorProfile
from django.contrib.auth.models import User




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
    # User-related fields
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    # Doctor-related fields
    specialization = forms.ChoiceField(choices=DoctorProfile.SPECIALIZATION_CHOICES)
    qualification = forms.CharField(max_length=200)
    years_of_experience = forms.IntegerField()
    clinic_address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    available_for_online = forms.BooleanField(required=False)
    
    class Meta:
        model = CustomUser  # Use CustomUser for authentication if you have a custom user model
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'  # Set user_type to 'doctor'

        if commit:
            user.save()
            # Create doctor profile linked to the user
            doctor_profile = DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                qualification=self.cleaned_data['qualification'],
                years_of_experience=self.cleaned_data['years_of_experience'],
                clinic_address=self.cleaned_data['clinic_address'],
                phone_number=self.cleaned_data['phone_number'],
                profile_picture=self.cleaned_data.get('profile_picture'),
                bio=self.cleaned_data.get('bio'),
                available_for_online=self.cleaned_data['available_for_online']
            )
        return user