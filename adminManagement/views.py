from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Student, FinishedEvent, EventCheckIn
from .forms import StudentForm, EventForm   
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import csv
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def view_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = EventCheckIn.objects.filter(event=event)
    return render(request, 'adminManagement/view_attendees.html', {'event': event, 'attendees': attendees})

# Add a student to attendees
def add_attendee(request, event_id):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = Student.objects.filter(student_id=student_id).first()
        event = get_object_or_404(Event, id=event_id)

        if student and not EventCheckIn.objects.filter(event=event, student=student).exists():
            EventCheckIn.objects.create(event=event, student=student)
            return redirect('view_attendees', event_id=event.id)
        else:
            return HttpResponse("Student not found or already checked in.")
    return redirect('view_attendees', event_id=event_id)

# Remove a student from attendees
def delete_attendee(request, event_id, student_id):
    attendee = EventCheckIn.objects.filter(event_id=event_id, student_id=student_id).first()

    if attendee:
        attendee.delete()
    return redirect('view_attendees', event_id=event_id)


def create_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        location_description = request.POST.get('location_description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Create and save the new Event instance
        event = Event(
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
            location_description=location_description,
            latitude=latitude,
            longitude=longitude,
        )
        event.save()

        return redirect('admin_dashboard')  # Redirect to the admin dashboard or events list

    return render(request, 'adminManagement/create_event.html')  # Render the event creation form

def add_student(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year_level = request.POST.get('year_level')
        section = request.POST.get('section')
        image = request.FILES.get('image')  # Handle the uploaded image

        # Check if the student ID already exists
        if Student.objects.filter(student_id=student_id).exists():
            return render(request, 'adminManagement/add_student.html', {
                'error_message': 'A student with this ID already exists.',
            })

        # Convert image to JPEG if not already in JPEG format
        if image and not image.name.endswith('.jpg'):
            img = Image.open(image)
            img = img.convert('RGB')  # Convert to RGB for JPEG format

            # Save the image in memory as JPEG
            img_io = BytesIO()
            img.save(img_io, format='JPEG')

            # Create a new InMemoryUploadedFile with the converted image
            image = InMemoryUploadedFile(
                img_io,  # File object
                'ImageField',  # Field name
                f"{image.name.split('.')[0]}.jpg",  # New file name
                'image/jpeg',  # Content type
                sys.getsizeof(img_io),  # File size
                None  # Optional charset
            )

        # Create a new student entry
        new_student = Student(
            name=name,
            student_id=student_id,
            course=course,
            year_level=year_level,
            section=section,
            image=image,  # Save the (converted) image
        )
        new_student.save()

        return redirect('admin_dashboard')  # Redirect back to the dashboard

    return render(request, 'adminManagement/add_student.html')  # Render the add student page

# View for editing an existing student
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to dashboard after editing
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'adminManagement/edit_student.html', {'form': form, 'student': student})

# View for deleting a student (this was already created)
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('admin_dashboard')



@login_required
def admin_dashboard(request):
    students = Student.objects.all()
    events = Event.objects.all()
    finishedEvents = FinishedEvent.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # Include request.FILES for file uploads like images
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StudentForm()

    return render(request, 'adminManagement/admin_dashboard.html', {
        'students': students,
        'events': events,
        'finished_events': finishedEvents,
        'student_form': form,  # Passing the form to the template
    })

def edit_event(request, event_id):
    # Get the event by ID or return a 404 if not found
    event = get_object_or_404(Event, id=event_id)

    # If it's a POST request, process the form data
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()  # Save the updated event
            return redirect('admin_dashboard')  # Redirect back to admin dashboard
    else:
        # If it's a GET request, pre-fill the form with the event's current data
        form = EventForm(instance=event)

    # Render the edit event template
    return render(request, 'adminManagement/edit_event.html', {'form': form, 'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('admin_dashboard')


def mark_event_as_finished(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    finished_event = FinishedEvent.objects.create(
        event_name=event.event_name,
        event_date=event.event_date,
        location_description=event.location_description,
    )

    checked_in_students = event.check_ins.all()
    
    
    for student in checked_in_students:
        finished_event.students_checked_in.add(student)
    
    finished_event.save()

    return redirect('admin_dashboard')


def finished_events(request):
    # Fetch all events that are finished (based on date or time comparison)
    current_time = timezone.now()
    finished_events = Event.objects.filter(event_date__lt=current_time.date())  # Assuming event is finished by date
    
    return render(request, 'mainPage/finished_events.html', {'finished_events': finished_events})



def view_finished_event_attendees(request, event_id):
    # Retrieve the finished event and all its details
    finished_event = get_object_or_404(FinishedEvent, id=event_id)
    
    # Get all students who attended the finished event
    attendees = finished_event.students_checked_in.all()
    
    # Prepare context data for the template
    context = {
        'finished_event': finished_event,
        'attendees': attendees,
    }
    
    # Render the finished event details and attendees in the new template
    return render(request, 'adminManagement/view_finished_attendees.html', context)

def delete_finished_event(request, event_id):
    # Get the FinishedEvent by ID or return a 404 error if not found
    finished_event = get_object_or_404(FinishedEvent, id=event_id)

    if request.method == 'POST':
        finished_event.delete()  # Deletes the finished event
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after deletion

    return redirect('admin_dashboard')  # Redirect if not a POST request

def download_event_excel(request, event_id):
    try:
        # Query the FinishedEvent model
        finished_event = FinishedEvent.objects.get(id=event_id)
    except FinishedEvent.DoesNotExist:
        raise Http404("Event matching query does not exist.")
    
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{finished_event.event_name}_attendees.csv"'
    
    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Name', 'Student ID'])

    # Get the students who checked in
    for student in finished_event.students_checked_in.all():
        writer.writerow([student.name, student.student_id])

    return response

