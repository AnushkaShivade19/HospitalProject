from django.db import models
from doctors.models import DoctorProfile
from accounts.models import Patient  # Adjust if your Patient app is named differently

class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE ,related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE ,related_name='prescriptions')
    date_issued = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    medications = models.TextField()
    notes = models.TextField(blank=True)
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True)

    def __str__(self):
        return f"Prescription {self.id} - {self.doctor.user.get_full_name()} to {self.patient.user.get_full_name()}"
