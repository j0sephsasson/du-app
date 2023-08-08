// TIMELINE SECTION 
const timelineItems = document.querySelectorAll('.timeline-item');
const timelineIndicator = document.querySelector('.timeline-indicator');

timelineItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        // Remove active class from all items and hide all case cards
        timelineItems.forEach(item => {
            item.classList.remove('active');
            const caseCard = item.querySelector('.case-card');
            caseCard.classList.add('hidden');
        });

        // Add active class to the clicked item and show the case card
        item.classList.add('active');
        const caseCard = item.querySelector('.case-card');
        caseCard.classList.remove('hidden');

        // Update the timeline indicator width
        const newWidth = ((index + 1) / timelineItems.length) * 100;
        timelineIndicator.style.width = `${newWidth}%`;

        // Scroll to the selected item
        item.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest'
        });
    });
});

// Set the first timeline item as active by default
timelineItems[0].classList.add('active');
// Show the case card for the first timeline item
timelineItems[0].querySelector('.case-card').classList.remove('hidden');
// Set timeline indicator initial width
const newWidth = ((1) / timelineItems.length) * 100;
timelineIndicator.style.width = `${newWidth}%`;

// NAV
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('hamburger').addEventListener('click', function () {
        document.getElementById('dropdown').classList.remove('hidden');
        document.getElementById('dropdown').classList.add('flex');
    });
    document.getElementById('close').addEventListener('click', function () {
        document.getElementById('dropdown').classList.add('hidden');
        document.getElementById('dropdown').classList.remove('flex');
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownLinks = document.querySelectorAll('#dropdown a');
    const dropdown = document.getElementById('dropdown');

    dropdownLinks.forEach((link) => {
        link.addEventListener('click', () => {
            dropdown.classList.toggle('hidden');
        });
    });
});

function goToHome() {
    window.location.href = '/';
};

// Modal form
// Get all elements with the 'openModalBtn' class
var openModalBtns = document.getElementsByClassName('openModalBtn');

// Add a click event listener to each button
for (var i = 0; i < openModalBtns.length; i++) {
    openModalBtns[i].addEventListener('click', function (e) {
        openModal(e);
    });
    openModalBtns[i].addEventListener('touchstart', function (e) {
        openModal(e);
    });
}

function openModal(e) {
    e.preventDefault();
    document.getElementById('modal').style.display = 'block';
}

window.addEventListener('click', function (e) {
    closeModal(e);
});
window.addEventListener('touchstart', function (e) {
    closeModal(e);
});

function closeModal(e) {
    if (e.target.id === 'modal') {
        document.getElementById('modal').style.display = 'none';
    }
}

document.getElementById('accessForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Hide the submit button and show the spinner
    const submitButton = document.querySelector('.submit-button');
    submitButton.style.display = 'none';

    const formData = new FormData(event.target);
    fetch('/send_email', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Clear the form fields
        event.target.reset();

        // After getting the response, show the submit button and hide the spinner
        submitButton.style.display = 'inline-block';

    })
    .catch(error => {
        // Show the submit button and hide the spinner
        submitButton.style.display = 'inline-block';

        console.error('There was an error!', error);
        alert(error);
    });
});