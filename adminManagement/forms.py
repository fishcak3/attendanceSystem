from django import forms
from .models import Student, Event

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'image']  # Fields for the Student model

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_date', 'event_time', 'location_description',]