from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from doctors.models import DoctorProfile, DoctorSchedule, TimeOff
from datetime import datetime, timedelta, time as djangotime
from django.shortcuts import render, redirect
from .models import DoctorSchedule, Appointment
from .forms import DoctorScheduleForm,SpecializationFilterForm
from datetime import date
from django.http import JsonResponse
from django.contrib.auth import get_user_model
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
def book_appointment(request):
    # Step 1: Get all predefined specializations
    specializations = [choice[0] for choice in DoctorProfile.SPECIALIZATION_CHOICES]

    # Step 2: Get selected specialization & doctors in that field
    selected_specialization = request.GET.get('specialization') or request.POST.get('specialization')
    doctors = DoctorProfile.objects.filter(specialization=selected_specialization) if selected_specialization else []

    # Step 3: Get the selected doctor and their available slots
    selected_doctor_id = request.GET.get('doctor') or request.POST.get('doctor_id')
    selected_doctor = DoctorProfile.objects.filter(id=selected_doctor_id).first() if selected_doctor_id else None
    slots = DoctorSchedule.objects.filter(doctor=selected_doctor) if selected_doctor else None

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        reason = request.POST.get('reason', '')

        # Check for missing information
        if not (selected_doctor and date_str and time_str):
            messages.error(request, "Please select specialization, doctor, date, and time.")
            return redirect('book_appointment')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect('book_appointment')

        # Check if the selected time slot is available
        available_slots = get_available_slots(selected_doctor, date_obj)
        if time_obj not in available_slots:
            messages.error(request, "This slot is no longer available.")
            return redirect('book_appointment')

        # Save the appointment
        Appointment.objects.create(
            patient=request.user,
            doctor=selected_doctor,
            date=date_obj,
            time=time_obj,
            reason=reason
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('my_appointments')

    return render(request, 'appointments/book_appointment.html', {
        'specializations': specializations,
        'selected_specialization': selected_specialization,
        'doctors': doctors,
        'selected_doctor': selected_doctor,
        'slots': slots
    })

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
def choose_specialization(request):
    form = SpecializationFilterForm(request.GET or None)
    doctors = None

    if form.is_valid():
        specialization = form.cleaned_data['specialization']
        doctors = DoctorProfile.objects.filter(specialization=specialization)

    return render(request, 'appointments/choose_doctor.html', {
        'form': form,
        'doctors': doctors,
    })
    
User = get_user_model()

def get_doctors_by_specialization(request):
    specialization = request.GET.get('specialization')
    doctors = DoctorProfile.objects.filter(specialization=specialization).select_related('user')
    doctor_list = [
        {
            'id': doctor.id,
            'name': f"{doctor.user.first_name} {doctor.user.last_name or ''}".strip()
        }
        for doctor in doctors
    ]
    return JsonResponse({'doctors': doctor_list})