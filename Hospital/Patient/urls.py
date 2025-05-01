from django.urls import path
from . import views

urlpatterns = [
    path('prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
]
