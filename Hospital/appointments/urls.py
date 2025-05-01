from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('', views.appointment_list, name='appointment_list'),  # list of appointments
    path('book/', views.book_appointment, name='book_appointment'),
    path('<int:appointment_id>/detail/', views.appointment_detail, name='appointment_detail'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
