from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment

@login_required
def book_appointment(request):
    if request.user.user_type != 'patient':
        return redirect('dashboard')  # restrict access

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def my_appointments(request):
    if request.user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.none()

    return render(request, 'appointments/list.html', {'appointments': appointments})
