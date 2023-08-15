from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session, current_app
import time
from werkzeug.utils import secure_filename
import os
import sys
import requests
from io import BytesIO
from dotenv import load_dotenv
import base64
import logging
from traceback import format_exc
from datetime import datetime
from rq import Queue
from rq.job import NoSuchJobError
from worker import r
from rq.job import Job
from tasks import process_upload
import json
from extensions import mail
from flask_mail import Message

# Configure logging
logging.basicConfig(level=logging.INFO)

## need to push again heroku was down and last push failed
load_dotenv()

app = Flask(__name__)

# Configure session
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['SESSION_PERMANENT'] = False  # Session data is not permanent
app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookie

# Configure Mail
app.config['MAIL_SERVER'] = 'mail.privateemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# init flask_mail so we can use it in our app
mail.init_app(app)

# Initialize RQ
q = Queue(connection=r, default_timeout=300)

def process_result_string(result_string, fields):
    """
    Process the result string to combine it with the corresponding fields.
    
    Args:
        result_string (str): The result string containing answers separated by '---------------'.
        fields (list): A list of field names.
        
    Returns:
        str: A formatted string with fields combined with their respective answers.
    """
    # Split the string using the separator and strip white spaces
    answers = [answer.strip() for answer in result_string.split("---------------") if answer.strip()]

    # Combine fields and answers
    combined = [f"{field}: {answer}" for field, answer in zip(fields, answers)]
    
    return "\n".join(combined)


@app.route('/')
def index():
    """
    Render the main index page.

    Returns:
        str: Rendered index.html template.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    Process uploaded PDF document

    Returns:
        str: Response message and success indication
    """
    try:
        logging.info('Processing upload request')
        
        if 'file' not in request.files:
            logging.error('No file part in request')
            return jsonify({"success": False, "message": "No file part"})

        file = request.files['file']
        file_contents = file.read()

        fields_str = request.form['fields']
        fields = json.loads(fields_str) # decode the JSON string to a list
        fields = ", ".join(fields) # join into comma separated string
        print(fields)

        if file.filename == '':
            logging.error('No file selected for uploading')
            return jsonify({"success": False, "message": "No file selected for uploading"})

        if file:
            filename = secure_filename(file.filename)

            # Offload the file processing to the RQ worker
            job = q.enqueue(process_upload, file_contents, filename, fields)
            return jsonify({
                "success": True,
                "message": "File is being processed",
                "job_id": job.get_id()
            })
    except Exception as e:
        logging.error('Exception occurred', exc_info=True)
        return jsonify({"success": False, "message": "An error occurred while processing the request"})
    
@app.route('/job/status/<job_id>', methods=['GET'])
def job_status(job_id):
    """
    Check the status of a job by its job_id.
    
    Args:
    - job_id (str): The ID of the job.

    Returns:
    - dict: The status of the job.
    """
    try:
        logging.info(f'Fetching job with id: {job_id}')
        job = Job.fetch(job_id, connection=r)
    except NoSuchJobError:
        logging.error(f'No such job: {job_id}')
        return {"success": False, "message": f"No such job: {job_id}"}
    except Exception as e:
        logging.error('Exception occurred while fetching job status', exc_info=True)
        return {"success": False, "message": "An error occurred while checking the job status"}

    if job.is_finished:
        logging.info(f'Job {job_id} has finished')
        return {"status": "finished"}
    elif job.is_queued:
        logging.info(f'Job {job_id} is in the queue')
        return {"status": "queued"}
    elif job.is_started:
        logging.info(f'Job {job_id} has started')
        return {"status": "started"}
    elif job.is_failed:
        logging.info(f'Job {job_id} has failed')
        return {"status": "failed"}
    else:
        logging.warning(f'Job {job_id} status is unknown')
        return {"status": "unknown"}

@app.route('/job/result/<job_id>', methods=['GET'])
def job_result(job_id):
    """
    Get the result of a job by its job_id.
    
    Args:
    - job_id (str): The ID of the job.

    Returns:
    - dict: The result of the job or an error message.
    """
    try:
        logging.info(f'Fetching result for job id: {job_id}')
        job = Job.fetch(job_id, connection=r)
    except NoSuchJobError:
        logging.error(f'No such job: {job_id}')
        return {"success": False, "message": f"No such job: {job_id}"}
    except Exception as e:
        logging.error('Exception occurred while fetching job result', exc_info=True)
        return {"success": False, "message": "An error occurred while fetching the job result"}

    if job.is_finished:
        if job.result.get("success"):
            logging.info(f'Successfully retrieved result for job id: {job_id}')

            # Parse the 'final_result' as a JSON object
            parsed_result = json.loads(job.result.get("final_result"))
            result_string = parsed_result.get("result")

            # Convert the comma-separated fields into a list
            fields_list = job.result.get("fields").split(", ")
            
            final = process_result_string(result_string=result_string, fields=fields_list)

            logging.info(f'Data: {final}')
            return {"success":True, "final_result": final}
        else:
            logging.error(f'Error during processing for job id: {job_id}, Message: {job.result.get("message")}')
            return {"success": False, "message": "Error during processing", "error": job.result.get("message")}
    else:
        logging.info(f'Job {job_id} is not finished yet')
        return {"success": False, "message": "Job not finished"}
    
@app.route('/send_email', methods=['POST'])
def send_email():
    """
    Endpoint to send an email.

    If the request method is POST, it reads the 'name', 'email', and 'use_case' from the form,
    creates a message, sends it, and then returns a success message.
    Otherwise, it returns an error indicating the method is not allowed.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        use_case = request.form['use_case']

        # Create message
        msg = Message('New Form Submission', recipients=['sassonjoe66@gmail.com'])
        msg.body = f'Name: {name}\nEmail: {email}\nUse Case: {use_case}'

        # Send email
        mail.send(msg)

        return jsonify(message='Email sent successfully!')

    return jsonify(error='Method not allowed'), 405

if __name__ == '__main__':
    app.run(debug=True, port=5000)