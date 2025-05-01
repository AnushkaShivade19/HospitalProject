from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),  # Doctors listing page

    # Schedule-related URLs
    path('schedule/', views.doctor_schedule_list, name='doctor_schedule_list'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('schedule/<int:schedule_id>/edit/', views.edit_schedule, name='edit_schedule'),

    # Time-off URLs
    path('timeoff/', views.doctor_timeoff_list, name='doctor_timeoff_list'),
    path('timeoff/mark/', views.mark_time_off, name='mark_time_off'),
]
