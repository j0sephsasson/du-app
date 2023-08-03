from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session, current_app
import time
from werkzeug.utils import secure_filename
import os
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

# Get the current date and time
now = datetime.now()

# Convert the current date and time into a string format: 'Year-Month-Day_Hour-Minute-Second'
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create a filename for log file
log_filename = f'logs/app_{date_time}.log'

# Create a logger
logger = logging.getLogger('app')

# Set logger level
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler(log_filename)

# Set a format for the messages
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Set the format for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

load_dotenv()

app = Flask(__name__)

# Initialize RQ
q = Queue(connection=r)

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
        logger.info('Processing upload request')
        
        if 'file' not in request.files:
            logger.error('No file part in request')
            return jsonify({"success": False, "message": "No file part"})

        file = request.files['file']
        file_contents = file.read()
        fields = request.form['fields']

        if file.filename == '':
            logger.error('No file selected for uploading')
            return jsonify({"success": False, "message": "No file selected for uploading"})

        if file:
            filename = secure_filename(file.filename)

            # Offload the file processing to the RQ worker
            job = q.enqueue(process_upload, file_contents, filename)
            return jsonify({
                "success": True,
                "message": "File is being processed",
                "job_id": job.get_id()
            })
    except Exception as e:
        logger.error('Exception occurred', exc_info=True)
        return jsonify({"success": False, "message": "An error occurred while processing the request"})
    
@app.route('/job/status/<job_id>', methods=['GET'])
def job_status(job_id):
    """
    Check the status of a job
    """
    try:
        logger.info(f'Fetching job with id: {job_id}')
        job = Job.fetch(job_id, connection=r)
    except NoSuchJobError:
        logger.error(f'No such job: {job_id}')
        return {"success": False, "message": f"No such job: {job_id}"}
    except Exception as e:
        logger.error('Exception occurred while fetching job status', exc_info=True)
        return {"success": False, "message": "An error occurred while checking the job status"}

    if job.is_finished:
        logger.info(f'Job {job_id} has finished')
        return {"status": "finished"}
    elif job.is_queued:
        logger.info(f'Job {job_id} is in the queue')
        return {"status": "queued"}
    elif job.is_started:
        logger.info(f'Job {job_id} has started')
        return {"status": "started"}
    elif job.is_failed:
        logger.info(f'Job {job_id} has failed')
        return {"status": "failed"}
    else:
        logger.warning(f'Job {job_id} status is unknown')
        return {"status": "unknown"}

@app.route('/job/result/<job_id>', methods=['GET'])
def job_result(job_id):
    """
    Get the result of a job
    """
    try:
        logger.info(f'Fetching result for job id: {job_id}')
        job = Job.fetch(job_id, connection=r)
    except NoSuchJobError:
        logger.error(f'No such job: {job_id}')
        return {"success": False, "message": f"No such job: {job_id}"}
    except Exception as e:
        logger.error('Exception occurred while fetching job result', exc_info=True)
        return {"success": False, "message": "An error occurred while fetching the job result"}

    if job.is_finished:
        if job.result.get("success"):
            logger.info(f'Successfully retrieved result for job id: {job_id}')
            logger.info(f'Data: {job.result.get("ocr_result")}')
            return {"ocr_result": job.result.get("ocr_result")}
        else:
            logger.error(f'Error during processing for job id: {job_id}, Message: {job.result.get("message")}')
            return {"success": False, "message": "Error during processing", "error": job.result.get("message")}
    else:
        logger.info(f'Job {job_id} is not finished yet')
        return {"success": False, "message": "Job not finished"}


if __name__ == '__main__':
    app.run(debug=True, port=5000)