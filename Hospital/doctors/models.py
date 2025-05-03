from django.db import models
from django.conf import settings  # Correct import

class DoctorProfile(models.Model):
    SPECIALIZATION_CHOICES = [
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('neurology', 'Neurology'),
    ('orthopedics', 'Orthopedics'),
    ('pediatrics', 'Pediatrics'),
    ('psychiatry', 'Psychiatry'),
    ('radiology', 'Radiology'),
    ('oncology', 'Oncology'),
    ('gastroenterology', 'Gastroenterology'),
    ('gynecology', 'Gynecology & Obstetrics'),
    ('urology', 'Urology'),
    ('nephrology', 'Nephrology'),
    ('endocrinology', 'Endocrinology'),
    ('pulmonology', 'Pulmonology'),
    ('ophthalmology', 'Ophthalmology'),
    ('ent', 'ENT (Ear, Nose, Throat)'),
    ('anesthesiology', 'Anesthesiology'),
    ('general_surgery', 'General Surgery'),
    ('plastic_surgery', 'Plastic Surgery'),
    ('vascular_surgery', 'Vascular Surgery'),
    ('rheumatology', 'Rheumatology'),
    ('infectious_diseases', 'Infectious Diseases'),
    ('immunology', 'Immunology'),
    ('hematology', 'Hematology'),
    ('sports_medicine', 'Sports Medicine'),
    ('geriatrics', 'Geriatrics'),
    ('family_medicine', 'Family Medicine'),
    ('internal_medicine', 'Internal Medicine'),
    ('pain_management', 'Pain Management'),
    ('rehabilitation', 'Physical Medicine & Rehabilitation'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    years_of_experience = models.PositiveIntegerField()
    clinic_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    available_for_online = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"
class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}"

class TimeOff(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.doctor} off on {self.date}"
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return self.name
