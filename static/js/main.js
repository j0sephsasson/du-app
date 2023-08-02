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
var formDataState = {
    file: null,
    fields: []
};

document.getElementById('uploadContainer').addEventListener('click', function (e) {
    e.stopPropagation();
    document.getElementById('fileUpload').click();
});

document.getElementById('fileUpload').addEventListener('click', function (e) {
    e.stopPropagation();
});

$('#fileUpload').on('change', handleFileSelect);

$('#submitButton').on('click', function () {
    $("#submitButton").hide();
    if(formDataState.file && formDataState.fields.length > 0) {
        // Add class to make the containers collapse
        $("#uploadContainer, .demo-fields").addClass("container-collapsed");
        $("#loading").show();

        var form_data = new FormData();
        form_data.append('file', formDataState.file);
        form_data.append('fields', JSON.stringify(formDataState.fields));

        // Array of messages to show
        const messages = ['Uploading your document...', 'Running AI algorithms...', 'Extracting data...'];
        let messageIndex = 0;
        showMessage(messages[messageIndex]);

        // Start a timer to change the message every 3 seconds
        const messageInterval = setInterval(() => {
            messageIndex = (messageIndex + 1) % messages.length;
            showMessage(messages[messageIndex]);
        }, 3000);

        $.ajax({
            url: '/upload',
            dataType: 'text',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) {
                clearInterval(messageInterval);  // Clear the timer
                $("#uploadContainer, .demo-fields").fadeOut('slow', function() {
                    $("#loading").hide();
                    $(".demo-result").hide().html(response.message).slideDown('slow');
                });
            },
            error: function (response) {
                clearInterval(messageInterval);  // Clear the timer
                $("#loading").hide();
                // Remove the collapse class to show the containers again
                $("#uploadContainer, .demo-fields").removeClass("container-collapsed");
                alert('Error occurred during file upload!');
            }
        });
    } else {
        alert("Please upload a file and add extraction fields before submitting");
        location.reload();
    }
});

const flashMessage = document.querySelector('.flash-message');
function showMessage(message) {
    flashMessage.textContent = message;
    flashMessage.classList.add('active');
  
    // Hide after 3 seconds
    setTimeout(() => {
        flashMessage.classList.remove('active');
    }, 3000);
}

function handleFileSelect(evt) {
    var file = evt.target.files[0];
    var reader = new FileReader();

    if (file) {
        formDataState.file = file;
        if (file.type.match('image.*')) {
            reader.onload = (function () {
                return function (e) {
                    $('#uploadContainer').html(['<img src="', e.target.result, '" title="', escape(file.name), '"/>'].join(''));
                };
            })(file);
        } else if (file.type.match('application/pdf')) {
            var fileURL = URL.createObjectURL(file);
            $('#uploadContainer').html('<iframe src="' + fileURL + '"></iframe>');
        } else {
            reader.onload = (function () {
                return function (e) {
                    $('#uploadContainer').text(e.target.result);
                };
            })(file);
        }

        reader.readAsDataURL(file);

        if (formDataState.fields.length > 0) {
            document.getElementById('submitBtn').style.display = "block";
        }
    }
}

$("#fieldInput").on('keyup', function (event) {
    if (event.key === "Enter") {
        var value = this.value.trim();
        if (value) {
            formDataState.fields.push(value);
            var fieldContainer = $("<div class='field'></div>");
            var fieldText = $("<p></p>").text(value);
            var deleteIcon = $("<i class='fa fa-times'></i>").on('click', function () {
                $(this).parent().remove();
                formDataState.fields = formDataState.fields.filter(function(field) {
                    return field !== value;
                });
                if ($("#fieldsContainer").children().length === 0) {
                    $("#fieldPrompt, .field-icon").show();
                    $("#extractionFields, #submitButton").hide();
                }
            });

            fieldContainer.append(fieldText, deleteIcon);
            $("#fieldsContainer").append(fieldContainer);
            this.value = "";

            if ($("#fieldsContainer").children().length === 1) {
                $("#fieldPrompt, .field-icon").hide();
                $("#extractionFields, #submitButton").show();
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