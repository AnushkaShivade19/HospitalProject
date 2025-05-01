from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_view, name='patients'), 
    path('prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
]
