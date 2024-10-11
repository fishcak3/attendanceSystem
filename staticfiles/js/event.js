function checkLocationAndRedirect(eventLat, eventLon, eventId) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const studentLat = position.coords.latitude;
            const studentLon = position.coords.longitude;

            // Compare the locations here (client-side check or send to server)
            const distance = calculateDistance(studentLat, studentLon, eventLat, eventLon);

            // Set the maximum allowed distance (e.g., 100 meters)
            const maxDistance = 1.0; // Approx. 1000 meters in degrees

            if (distance <= maxDistance) {
                // If within the allowed range, redirect to the event check-in page
                window.location.href = `/check-in/${eventId}/`;
            } else {
                document.getElementById('location-status').innerHTML = "You are too far from the event location.";
            }
        }, function() {
            document.getElementById('location-status').innerHTML = "Geolocation is not available.";
        });
    } else {
        document.getElementById('location-status').innerHTML = "Geolocation is not supported by this browser.";
    }
}

// Haversine formula for calculating distance between two coordinates
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        0.5 - Math.cos(dLat)/2 + 
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        (1 - Math.cos(dLon)) / 2;

    return R * 2 * Math.asin(Math.sqrt(a)); // Distance in kilometers
}
