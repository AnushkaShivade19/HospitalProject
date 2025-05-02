from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from doctors.models import DoctorProfile, DoctorSchedule, TimeOff
from datetime import datetime, timedelta, time as djangotime
from django.shortcuts import render, redirect
from .models import DoctorSchedule, Appointment
from .forms import DoctorScheduleForm
from datetime import date
@login_required
def appointment_list(request):
    # List the logged-in patient's appointments
    appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'time')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def doctor_available_slots(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    date_str = request.GET.get('date')
    available_slots = []

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            available_slots = get_available_slots(doctor, date_obj)
        except ValueError:
            messages.error(request, "Invalid date format.")

    return render(request, 'appointments/doctor_slots.html', {
        'doctor': doctor,
        'available_slots': available_slots,
        'selected_date': date_str,
    })

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        reason = request.POST.get('reason', '')

        if not date_str or not time_str:
            messages.error(request, "Date and time are required.")
            return redirect('doctor_available_slots', doctor_id=doctor_id)

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        # Check if the slot is still available
        available_slots = get_available_slots(doctor, date_obj)
        if time_obj not in available_slots:
            messages.error(request, "This slot is no longer available.")
            return redirect('doctor_available_slots', doctor_id=doctor_id)

        # Create appointment
        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date_obj,
            time=time_obj,
            reason=reason
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('appointment_list')

    return redirect('doctor_available_slots', doctor_id=doctor_id)


def get_available_slots(doctor, date):
    """
    Returns a list of available time slots (as time objects) for the doctor on a specific date.
    Excludes slots where appointments already exist and when doctor is off.
    """
    day_of_week = date.weekday()

    # Check if doctor is off that day
    if TimeOff.objects.filter(doctor=doctor, date=date).exists():
        return []

    schedules = DoctorSchedule.objects.filter(doctor=doctor, day_of_week=day_of_week)

    existing_appointments = Appointment.objects.filter(doctor=doctor, date=date)
    booked_times = set([appt.time for appt in existing_appointments])

    slots = []

    SLOT_DURATION_MINUTES = 30  # change as needed

    for schedule in schedules:
        current_time = datetime.combine(date, schedule.start_time)
        end_time = datetime.combine(date, schedule.end_time)

        while current_time + timedelta(minutes=SLOT_DURATION_MINUTES) <= end_time:
            slot_time = current_time.time()
            if slot_time not in booked_times:
                slots.append(slot_time)
            current_time += timedelta(minutes=SLOT_DURATION_MINUTES)

    return slots
# appointments/views.py



def add_schedule(request):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_schedule')
    else:
        form = DoctorScheduleForm()
    return render(request, 'appointments/add_schedule.html', {'form': form})


def view_schedule(request):
    today = request.GET.get('date', date.today())
    schedules = DoctorSchedule.objects.filter(date=today)
    appointments = Appointment.objects.filter(date=today)

    context = {
        'schedules': schedules,
        'appointments': appointments,
        'date': today,
        'appointments_count': appointments.count()
    }
    return render(request, 'appointments/view_schedule.html', context)

def doctor_schedule_list(request):
    schedules = DoctorSchedule.objects.all()
    return render(request, 'appointments/schedule_list.html', {'schedules': schedules})

def appointment_detail(request, appointment_id):
    return render(request, 'appointments/appointment_detail.html', {'appointment_id': appointment_id})

def cancel_appointment(request, appointment_id):
    # Dummy response for now
    return render(request, 'appointments/cancel_appointment.html', {'appointment_id': appointment_id})
@login_required
def my_appointments(request):
    # Fetch appointments for the logged-in user
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date')

    # If no appointments, show a message
    if not appointments:
        no_appointments_message = "You have no upcoming appointments."
    else:
        no_appointments_message = None

    # Render the template with appointments data
    return render(
        request, 
        'appointments/my_appointments.html', 
        {'appointments': appointments, 'no_appointments_message': no_appointments_message}
    )