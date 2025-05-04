from django.contrib import admin
from .models import CustomUser, Patient, Prescription, MedicalRecord, InsuranceDetail, Referral, Department, Service
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone_number', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(MedicalRecord)
admin.site.register(InsuranceDetail)
admin.site.register(Referral)
admin.site.register(Department)
admin.site.register(Service)
