from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),
    path('add/', views.add_prescription, name='add_prescription'),
]
