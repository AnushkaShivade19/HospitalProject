from django.shortcuts import render, redirect
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



@user_passes_test(is_admin_user)
@login_required
def register_doctor_internal(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'doctor'  # assuming your model has this field
            user.save()

            # Create DoctorProfile here (you can adjust these fields as needed)
            DoctorProfile.objects.create(
                user=user,
                specialization=request.POST.get('specialization', ''),
                qualification=request.POST.get('qualification', ''),
                years_of_experience=request.POST.get('years_of_experience', 0),
                clinic_address=request.POST.get('clinic_address', ''),
                phone_number=request.POST.get('phone_number', ''),
                # Optionally add profile_picture, bio, etc.
            )

            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'accounts/register_doctor.html', {'form': form})


@login_required
def doctor_dashboard(request):
    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        messages.error(request, "You don't have a doctor profile yet. Please register as a doctor.")
        return redirect('home')  # or wherever you'd like

    schedules = DoctorSchedule.objects.filter(doctor=doctor_profile)
    timeoffs = TimeOff.objects.filter(doctor=doctor_profile)
    appointments = Appointment.objects.filter(doctor=doctor_profile)

    context = {
        'schedules': schedules,
        'timeoffs': timeoffs,
        'appointments': appointments,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)
@login_required
def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html')
