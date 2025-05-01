from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
]
