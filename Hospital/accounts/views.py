from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientRegistrationForm, DoctorRegistrationForm


def home(request):
    return render(request, 'home.html')

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

def custom_logout_view(request):
    logout(request)
    return redirect('login')

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'accounts/register_patient.html', {'form': form})

def is_admin_user(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == 'admin')

@user_passes_test(is_admin_user)
@login_required
def register_doctor_internal(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'accounts/register_doctor.html', {'form': form})

@login_required
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html')
