"""
URL configuration for attendanceSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainPage import views as mainpage_views
from adminManagement import views as admin_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin-management/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-management/add-student/', admin_views.add_student, name='add_student'),
    path('admin-management/edit-student/<int:student_id>/', admin_views.edit_student, name='edit_student'),
    path('admin-management/delete-student/<int:student_id>/', admin_views.delete_student, name='delete_student'),
    path('admin-management/create-event/', admin_views.create_event, name='create_event'),
    path('admin-management/delete-event/<int:event_id>/', admin_views.delete_event, name='delete_event'),
    path('admin-management/edit_event/<int:event_id>/', admin_views.edit_event, name='edit_event'),
    path('admin-management/view-attendees/<int:event_id>/', admin_views.view_attendees, name='view_attendees'),
    path('admin-management/mark-event-as-finished/<int:event_id>/', admin_views.mark_event_as_finished, name='mark_event_as_finished'),
    path('admin-management/view-finished-attendees/<int:event_id>/', admin_views.view_finished_event_attendees, name='view_finished_attendees'),
    path('admin-management/delete-finished-event/<int:event_id>/', admin_views.delete_finished_event, name='delete_finished_event'),
    path('admin-management/download-event/<int:event_id>/', admin_views.download_event_excel, name='download_event_excel'),
    path('', mainpage_views.home, name='home'),
    path('event-list/', include('mainPage.urls')),
    path('check-in/<int:event_id>/', mainpage_views.check_in, name='check_in'),
    path('check-in-success/<int:event_id>/', mainpage_views.check_in_success, name='check_in_success'),

] 
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
