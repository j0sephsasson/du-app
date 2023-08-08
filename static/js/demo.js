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

// When submit button is clicked, process form
$('#submitButton').on('click', function () {
    processForm();
});

async function processForm() {
    $("#submitButton").hide();
    if (!formDataState.file || formDataState.fields.length === 0) {
        alert("Please upload a file and add extraction fields before submitting");
        location.reload();
        return;
    }

    $("#uploadContainer, .demo-fields").addClass("container-collapsed");
    $("#loading").show();

    // Flash messages
    let messages = ['This process can take up to two and a half minutes...', 'Uploading your document...', 'Waking up your AI model...', 'Running AI algorithms...', 'Extracting data...'];
    let messageIndex = 0;
    let timeouts = [];
    let flashMessage = document.querySelector('.flash-message');

    function showMessage() {
        // Show the message
        flashMessage.textContent = messages[messageIndex];
        flashMessage.classList.add('active');

        // Schedule the message to be hidden after 16 seconds
        timeouts.push(setTimeout(() => {
            flashMessage.classList.remove('active');

            // Increase the index or stop if the end is reached
            messageIndex++;
            if (messageIndex < messages.length) {
                // Schedule the next message to be shown in 1.5 seconds
                timeouts.push(setTimeout(showMessage, 1500));
            }
        }, 16000));
    }

    function stopShowingMessages() {
        // Clear timeouts
        timeouts.forEach(clearTimeout);

        // Fade out the last message and hide it
        $(flashMessage).fadeOut('slow', function(){
            flashMessage.classList.remove('active');
        });
    }

    showMessage();

    try {
        const response = await uploadFile(formDataState.file, formDataState.fields);

        if (response.success) {
            await waitForJob(response.job_id);
            const jobResult = await getJobResult(response.job_id);
            stopShowingMessages(); // Clear messages when the job results are available
            showResult(jobResult);
        } else {
            stopShowingMessages(); // Clear messages when there's an upload error
            showUploadError();
        }
    } catch (error) {
        stopShowingMessages(); // Clear messages when there's an error
        if (error.message === 'JobStatusError') {
            showJobStatusError();
        } else {
            showGenericError();
        }
    }
}

// AJAX request to upload file
function uploadFile(file, fields) {
    let form_data = new FormData();
    form_data.append('file', file);
    form_data.append('fields', JSON.stringify(fields));

    return $.ajax({
        url: '/upload',
        dataType: 'text',
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
    }).then(JSON.parse)
    .done(function (response) {
        return response;
    })
    .fail(function (error) {
        throw error;
    });
}

// Wait for the job to finish
async function waitForJob(job_id) {
    let jobStatus;
    do {
        try {
            await new Promise(r => setTimeout(r, 2000));  // Wait for 2 seconds before checking again
            jobStatus = await checkJobStatus(job_id);
        } catch (error) {
            console.error(`Error while checking job status for ${job_id}:`, error);
            throw new Error('JobStatusError');
        }
    } while (jobStatus.status === 'queued' || jobStatus.status === 'started');
}

// AJAX request to check job status
function checkJobStatus(job_id) {
    return $.get(`/job/status/${job_id}`);
}

// AJAX request to get job result
function getJobResult(job_id) {
    return $.get(`/job/result/${job_id}`).catch((error) => {
        console.error(`Error while getting job result for ${job_id}:`, error);
        showJobResultError();
    });
}

// Show error if checking job status failed
function showJobStatusError() {
    stopShowingMessages();
    $("#loading").hide();
    // Remove the collapse class to show the containers again
    $("#uploadContainer, .demo-fields").removeClass("container-collapsed");
    alert('Error occurred while checking job status!');
}

// Show error for any other unhandled exception
function showGenericError() {
    stopShowingMessages();
    $("#loading").hide();
    // Remove the collapse class to show the containers again
    $("#uploadContainer, .demo-fields").removeClass("container-collapsed");
    alert('An unexpected error occurred!');
}

// Show error if getting job result failed
function showJobResultError() {
    $("#loading").hide();
    // Remove the collapse class to show the containers again
    $("#uploadContainer, .demo-fields").removeClass("container-collapsed");
    alert('Error occurred while getting job result!');
}

// Show the result
function showResult(result) {
    $("#uploadContainer, .demo-fields").fadeOut('slow', function() {
        $("#loading").hide();
        if (result.success) {
            if ('final_result' in result) {
                $("#resultText").text(result.final_result);
            } else {
                $("#resultText").text("Results are not available");
            }
        } else {
            $("#resultText").text(result.message);
        }
        $(".demo-result").hide().slideDown('slow');
    });
}

// Show error if upload failed
function showUploadError() {
    $("#loading").hide();
    // Remove the collapse class to show the containers again
    $("#uploadContainer, .demo-fields").removeClass("container-collapsed");
    alert('Error occurred during file upload!');
}