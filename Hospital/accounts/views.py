from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from django.contrib import messages
from doctors.models import DoctorProfile, DoctorSchedule, TimeOff
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def custom_logout_view(request):
    logout(request)
    return redirect('home')  # or 'home', depending on where you want to redirect

def is_admin_user(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == 'admin')

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
            elif user.user_type == 'admin':
                return redirect('/admin/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Patient registration successful. You are now logged in.")
            login(request, user)  # Log the patient in directly
            return redirect('patient_dashboard')  # Redirect to patient dashboard
    else:
        form = PatientRegistrationForm()
    return render(request, 'accounts/register_patient.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
def register_doctor_internal(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the User object (doctor user)
            user = form.save()

            # Prevent duplicate DoctorProfile creation
            if DoctorProfile.objects.filter(user=user).exists():
                messages.error(request, "This user already has a doctor profile.")
                return redirect('doctor_dashboard')

            # Create the DoctorProfile
            doctor_profile = DoctorProfile.objects.create(
                user=user,
                specialization=form.cleaned_data.get('specialization'),
                qualification=form.cleaned_data.get('qualification'),
                years_of_experience=form.cleaned_data.get('years_of_experience'),
                clinic_address=form.cleaned_data.get('clinic_address'),
                phone_number=form.cleaned_data.get('phone_number'),
                profile_picture=form.cleaned_data.get('profile_picture'),  
                bio=form.cleaned_data.get('bio'),
            )

            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_dashboard')  # Or another success page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorRegistrationForm()

    return render(request, 'accounts/register_doctor.html', {'form': form})



@login_required
def doctor_dashboard(request):
    # Superusers should have access to all profiles
    if request.user.is_superuser:
        doctor = None
    else:
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            messages.error(request, "You are not registered as a doctor.")
            return redirect('home')

    schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('day_of_week') if doctor else []
    timeoffs = TimeOff.objects.filter(doctor=doctor).order_by('-date') if doctor else []
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date') if doctor else []

    context = {
        'schedules': schedules,
        'timeoffs': timeoffs,
        'appointments': appointments,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)

@login_required
def patient_dashboard(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'accounts/patient_dashboard.html', {'doctors': doctors})

# Register doctor view
