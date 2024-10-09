// Show and hide sections
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}

function confirmMarkEvent() {
    return confirm("Are you sure you want to mark this event as finished? This action cannot be undone.");
}

// Load data on page load
window.onload = function() {
    // Optionally, load any necessary data for the initial view
    showSection('students-section'); // Show students section by default
};


