from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('', views.appointment_list, name='appointment_list'),  # list of appointments
    #path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('<int:appointment_id>/detail/', views.appointment_detail, name='appointment_detail'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/doctor/<int:doctor_id>/slots/', views.doctor_available_slots, name='doctor_available_slots'),
    path('ajax/get-doctors/', views.get_doctors_by_specialization, name='get_doctors_by_specialization'),

]
