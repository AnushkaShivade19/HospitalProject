from django.contrib import admin
from .models import DoctorProfile, DoctorSchedule, TimeOff

admin.site.register(DoctorProfile)
admin.site.register(DoctorSchedule)
admin.site.register(TimeOff)
