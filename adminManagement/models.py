from django.db import models
from django.utils import timezone
import os

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.CharField(max_length=100, blank=True)
    year_level = models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], default=1)
    section = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
    def save(self, *args, **kwargs):
        # Change the image name to student_id if it has been uploaded
        if self.image:
            # Get the extension of the uploaded image
            ext = os.path.splitext(self.image.name)[1]  # Get the file extension
            # Create a new filename using student_id
            self.image.name = f"{self.student_id}{ext}"  # Set the new name
        super().save(*args, **kwargs)  # Call the original save method


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)
    location_description = models.CharField(blank=True, null=True, max_length=300)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    check_ins = models.ManyToManyField(Student, through='EventCheckIn')
    
    def __str__(self):
        return self.event_name
    

class EventCheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)


class FinishedEvent(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)  # Added event_time for clarity
    location_description = models.CharField(max_length=300)
    latitude = models.FloatField(blank=True, null=True)  # Optional latitude for geographic coordinates
    longitude = models.FloatField(blank=True, null=True)  # Optional longitude for geographic coordinates
    students_checked_in = models.ManyToManyField('Student', related_name='finished_events')

    def __str__(self):
        return f"{self.event_name} on {self.event_date}"

    def total_attendees(self):
        """Returns the total number of students who checked in."""
        return self.students_checked_in.count()
