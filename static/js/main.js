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