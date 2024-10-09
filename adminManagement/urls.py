from django.urls import path
from . import views
from django.shortcuts import get_object_or_404

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('mark-event-as-finished/<int:event_id>/', views.mark_event_as_finished, name='mark_event_as_finished'),
    path('download-event/<int:event_id>/', views.download_event_excel, name='download_event_excel'),
    path('view-attendees/<int:event_id>/add/', views.add_attendee, name='add_attendee'),
    path('view-attendees/<int:event_id>/delete/<int:student_id>/', views.delete_attendee, name='delete_attendee'),
    
]

