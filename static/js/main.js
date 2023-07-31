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

// DEMO SECTION
document.getElementById('uploadContainer').addEventListener('click', function () {
    document.getElementById('fileUpload').click();
}, false);

document.getElementById('fileUpload').addEventListener('change', handleFileSelect, false);

function handleFileSelect(evt) {
    var file = evt.target.files[0];
    var reader = new FileReader();

    if (file.type.match('image.*')) {
        reader.onload = (function () {
            return function (e) {
                document.getElementById('uploadContainer').innerHTML = ['<img src="', e.target
                    .result, '" title="', escape(file.name), '"/>'
                ].join('');
            };
        })(file);
    } else if (file.type.match('application/pdf')) {
        var fileURL = URL.createObjectURL(file);
        document.getElementById('uploadContainer').innerHTML = '<iframe src="' + fileURL + '"></iframe>';
    } else {
        reader.onload = (function () {
            return function (e) {
                document.getElementById('uploadContainer').textContent = e.target.result;
            };
        })(file);
    }

    reader.readAsDataURL(file);

    document.getElementById('submitBtn').style.display = "block";
}

document.querySelector("#fieldInput").addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        let value = this.value.trim();
        if (value) {
            let fieldContainer = document.createElement("div");
            fieldContainer.classList.add("field");
            let fieldText = document.createElement("p");
            fieldText.textContent = value;
            let deleteIcon = document.createElement("i");
            deleteIcon.classList.add("fa", "fa-times");
            deleteIcon.addEventListener("click", function () {
                this.parentNode.remove();
                if (document.querySelector("#fieldsContainer").children.length === 0) {
                    document.querySelector("#fieldPrompt").style.display = "block";
                    document.querySelector(".field-icon").style.display = "block";
                    document.querySelector("#extractionFields").style.display =
                    "none"; // Hide extraction fields text if no fields exist
                }
            });
            fieldContainer.append(fieldText, deleteIcon);
            document.querySelector("#fieldsContainer").append(fieldContainer);
            this.value = "";
            if (document.querySelector("#fieldsContainer").children.length === 1) {
                document.querySelector("#fieldPrompt").style.display = "none";
                document.querySelector(".field-icon").style.display = "none";
                document.querySelector("#extractionFields").style.display =
                "block"; // Show extraction fields text when a field is added
            }
        }
    }
});

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