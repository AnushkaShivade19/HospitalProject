from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from django.contrib import messages
from doctors.models import DoctorProfile, DoctorSchedule, TimeOff
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'home.html')


def custom_logout_view(request):
    logout(request)
    return redirect('home')  # or 'home', depending on where you want to redirect

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to login on failure
    else:
        return render(request, 'accounts/login.html')  # Show login form on GET
        
def is_admin_user(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == 'admin')


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
            form.save()
            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_dashboard')  # or wherever you want
        else:
            print(form.errors)  # Add this to debug form validation issues
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
