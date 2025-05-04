from django.db import models
from django.contrib.auth.models import AbstractUser
from doctors.models import DoctorProfile


# Custom User model to support multiple types of users (patients, doctors, admins)
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
# Model for storing patient details
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Patient {self.user.username}"

# Model for storing prescriptions issued by doctors
class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    medicine = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient.user.username} by Dr. {self.doctor.user.username}"

# Model for storing medical records for patients
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    record_date = models.DateField()
    diagnosis = models.CharField(max_length=200)
    treatment = models.TextField()
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Medical Record for {self.patient.user.username} - {self.record_date}"

# Model for storing insurance details for patients
class InsuranceDetail(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    insurance_provider = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=50)
    valid_until = models.DateField()

    def __str__(self):
        return f"Insurance for {self.patient.user.username} by {self.insurance_provider}"

# Model for storing referrals from doctors
class Referral(models.Model):
    referring_doctor = models.ForeignKey(DoctorProfile, related_name='referring_doctor', on_delete=models.CASCADE)
    referred_doctor = models.ForeignKey(DoctorProfile, related_name='referred_doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Referral: {self.patient.user.username} from Dr. {self.referring_doctor.user.username} to Dr. {self.referred_doctor.user.username}"

# Model for storing hospital departments
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Model for storing hospital services offered
class Service(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
