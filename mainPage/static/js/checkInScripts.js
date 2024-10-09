// Access the webcam and display the live feed
const video = document.getElementById('videoElement');
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Something went wrong accessing the webcam!", error);
        });
}

// Function to capture the image and submit the form
function captureAndSubmitFaceImage() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

    // Convert the canvas data to base64
    const imageData = canvas.toDataURL('image/png');
    document.getElementById('face_image').value = imageData;

    // Submit the form after setting the hidden image field
    document.getElementById('checkInForm').submit();
}

// Function to validate the form and then submit
function validateAndSubmit() {
    const studentIdField = document.getElementById('student_id');
    const errorMessage = document.getElementById('error-message');

    // Check if student ID is provided
    if (studentIdField.value.trim() === "") {
        // Display error message if student ID is missing
        errorMessage.style.display = 'block';
        return;
    } else {
        // Hide the error message if ID is provided
        errorMessage.style.display = 'none';

        // Proceed with capturing the face image and submitting the form
        captureAndSubmitFaceImage();
    }
}
