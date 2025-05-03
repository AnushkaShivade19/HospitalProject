from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import DoctorProfile
from .models import Prescription
from .forms import PrescriptionForm

@login_required
def prescription_list(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    prescriptions = Prescription.objects.filter(doctor=doctor)
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

@login_required
def add_prescription(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.doctor = doctor
            p.save()
            messages.success(request, "Prescription added.")
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions/add_prescription.html', {'form': form})
