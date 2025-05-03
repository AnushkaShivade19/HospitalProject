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
            # Save the form and create the user and profile
            form.save()
            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorRegistrationForm()

    return render(request, 'accounts/register_doctor.html', {'form': form})
@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)

    schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('day_of_week')
    timeoffs = TimeOff.objects.filter(doctor=doctor).order_by('-date')
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')

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
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the user first (Doctor)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password
            user.user_type = 'doctor'  # Set the user type to 'doctor'
            user.save()

            # Create the Doctor Profile
            doctor_profile = DoctorProfile.objects.create(
                user=user,
                specialization=form.cleaned_data['specialization'],
                qualification=form.cleaned_data['qualification'],
                years_of_experience=form.cleaned_data['years_of_experience'],
                clinic_address=form.cleaned_data['clinic_address'],
                phone_number=form.cleaned_data['phone_number'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                bio=form.cleaned_data.get('bio'),
                available_for_online=form.cleaned_data['available_for_online'],
            )

            return redirect('doctor_dashboard')  # Redirect to doctor dashboard after registration
    else:
        form = DoctorRegisterForm()

    return render(request, 'accounts/register_doctor.html', {'form': form})