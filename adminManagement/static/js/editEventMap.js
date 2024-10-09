// Get latitude and longitude from the input fields
let lat = document.getElementById('latitude').value || 15.0; // Default latitude if not provided
let lng = document.getElementById('longitude').value || 120.0; // Default longitude if not provided

// Initialize the map with the provided or default coordinates
let map = L.map('map').setView([lat, lng], 13);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add a draggable marker to the map
let marker = L.marker([lat, lng], { draggable: true }).addTo(map);

// Update the input fields when the marker is dragged
marker.on('dragend', function(event) {
    let position = marker.getLatLng();
    document.getElementById('latitude').value = position.lat;
    document.getElementById('longitude').value = position.lng;
});

// Allow the user to click on the map to move the marker and update the coordinates
map.on('click', function(event) {
    let location = event.latlng;
    marker.setLatLng(location);
    document.getElementById('latitude').value = location.lat;
    document.getElementById('longitude').value = location.lng;
});
