let map;
let marker;

function initMap() {
    // Initialize the map centered at a default location
    const defaultLocation = [15.921926605598918, -239.58581577623548]; // Replace with your desired default location

    map = L.map('map').setView(defaultLocation, 13); // Set initial map view

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add a marker to the map
    marker = L.marker(defaultLocation, { draggable: true }).addTo(map);

    // Update latitude and longitude when the marker is dragged
    marker.on('dragend', function (event) {
        const position = marker.getLatLng();
        document.getElementById('latitude').value = position.lat;
        document.getElementById('longitude').value = position.lng;
    });

    // Add a click event listener on the map
    map.on('click', function (event) {
        placeMarker(event.latlng);
    });
}

function placeMarker(location) {
    marker.setLatLng(location);
    document.getElementById('latitude').value = location.lat;
    document.getElementById('longitude').value = location.lng;
}

window.onload = initMap; // Initialize map on window load
