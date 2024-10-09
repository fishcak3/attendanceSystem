from django.contrib import admin
from .models import Event, Student, FinishedEvent

# Register models
admin.site.register(Event)
admin.site.register(Student)
admin.site.register(FinishedEvent)