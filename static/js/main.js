const timelineItems = document.querySelectorAll('.timeline-item');
const timelineIndicator = document.querySelector('.timeline-indicator');

timelineItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        // Remove active class from all items
        timelineItems.forEach(item => item.classList.remove('active'));

        // Add active class to the clicked item
        item.classList.add('active');

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