from adminManagement.models import Event, Student,EventCheckIn
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import base64
from django.http import HttpResponse
import numpy as np
import cv2
from deepface import DeepFace


def home(request):
    return render(request, 'mainPage/home.html')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'mainPage/event_list.html', {'events': events})


def check_in(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Get the student ID from the form data
        student_id = request.POST.get('student_id')
        student = Student.objects.filter(student_id=student_id).first()

        if not student:
            return HttpResponse("Student not found!")

        # Check if the student has already checked in
        if EventCheckIn.objects.filter(event=event, student=student).exists():
            return HttpResponse(f"{student.name} has already checked in for this event!")

        # Get the base64-encoded image from the POST request (captured via camera on check-in)
        face_image_data = request.POST.get('face_image')
        if not face_image_data:
            return HttpResponse("No image data provided!")

        # Decode the base64 image to a NumPy array using OpenCV
        format, imgstr = face_image_data.split(';base64,')  # Separate metadata and base64 data
        img_data = base64.b64decode(imgstr)
        np_arr = np.frombuffer(img_data, np.uint8)
        check_in_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Read as BGR

        # Detect if a face exists in the image using OpenCV's built-in face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_image = cv2.cvtColor(check_in_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return HttpResponse("No face detected in the image! Please try again.")

        try:
            # Perform face recognition using DeepFace
            result = DeepFace.verify(check_in_image, student.image.path, model_name='Facenet', distance_metric='euclidean_l2')

            if result["verified"]:
                # Create EventCheckIn instance and log the current time
                check_in_time = timezone.now()
                EventCheckIn.objects.create(event=event, student=student, check_in_time=check_in_time)

                return redirect('check_in_success', event_id=event.id)
            else:
                return HttpResponse("Face does not match!")
        except ValueError as e:
            return HttpResponse(f"Error during face processing: {str(e)}")

    return render(request, 'mainPage/check_in.html', {'event': event})


def check_in_success(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'mainPage/check_in_success.html', {'event': event})