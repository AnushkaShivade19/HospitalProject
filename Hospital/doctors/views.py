from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorProfile, DoctorSchedule, TimeOff
from .forms import DoctorScheduleForm, TimeOffForm
from .models import Doctor

@login_required
def doctor_schedule_list(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    schedules = DoctorSchedule.objects.filter(doctor=doctor)
    return render(request, 'doctors/schedule_list.html', {'schedules': schedules})

@login_required
def add_schedule(request):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Get the doctor profile linked to the user
    doctor = get_object_or_404(DoctorProfile, user=request.user)

    if request.method == 'POST':
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if day and start_time and end_time:
            DoctorSchedule.objects.create(
                doctor=doctor,
                day_of_week=day,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, "Schedule added successfully.")
            return redirect('doctor_schedule_list')  # Update with correct URL name

    return render(request, 'doctors/add_schedule.html', {'days_of_week': days_of_week})

@login_required
def edit_schedule(request, schedule_id):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    schedule = get_object_or_404(DoctorSchedule, id=schedule_id, doctor=doctor)
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated.")
            return redirect('doctor_schedule_list')  # You can redirect to your schedule list view here
    else:
        form = DoctorScheduleForm(instance=schedule)
    return render(request, 'doctors/edit_schedule.html', {'form': form})

@login_required
def doctor_timeoff_list(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    timeoffs = TimeOff.objects.filter(doctor=doctor)
    return render(request, 'doctors/timeoff_list.html', {'timeoffs': timeoffs})

@login_required
def mark_time_off(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    if request.method == 'POST':
        form = TimeOffForm(request.POST)
        if form.is_valid():
            timeoff = form.save(commit=False)
            timeoff.doctor = doctor
            timeoff.save()
            messages.success(request, "Time off marked.")
            return redirect('doctor_timeoff_list')
    else:
        form = TimeOffForm()
    return render(request, 'doctors/mark_time_off.html', {'form': form})


def doctor_list(request):
    doctors = Doctor.objects.all()  # Fetch all doctors
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})