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

# Get the current date and time
now = datetime.now()

# Convert the current date and time into a string format: 'Year-Month-Day_Hour-Minute-Second'
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create a filename for log file
log_filename = f'logs/app_{date_time}.log'

# Configure the logging
logging.basicConfig(filename=log_filename, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


load_dotenv()

app = Flask(__name__)

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
    logger = logging.getLogger('upload')
    try:
        logger.info('Processing upload request')
        
        if 'file' not in request.files:
            logger.error('No file part in request')
            return jsonify({"success": False, "message": "No file part"})

        file = request.files['file']
        fields = request.form['fields']

        if file.filename == '':
            logger.error('No file selected for uploading')
            return jsonify({"success": False, "message": "No file selected for uploading"})

        if file:
            filename = secure_filename(file.filename)
            logger.info(f'File "{filename}" received for uploading')

            # Prepare the request to the lambda URL
            api_url = os.getenv('LAMBDA_URL')
            file_ext = os.path.splitext(filename)[1]
            api_url += f"?file_ext={file_ext}"
            logger.info(f'Prepared API URL: {api_url}')

            file_obj = BytesIO(file.read())
            encoded_file = base64.b64encode(file_obj.getvalue()).decode()

            # Send the request and get the response
            logger.info('Sending request to Lambda function')
            response = requests.post(api_url, json={"body": encoded_file})

            # Process the response from Lambda function
            if response.status_code == 200:
                lambda_response = response.json()
                logger.info("SUCCESS: {}".format(lambda_response["ocr_result"]))
                return jsonify({
                    "success": True,
                    "message": "File successfully uploaded",
                    "ocr_result": lambda_response["ocr_result"]
                })
            else:
                logger.error("ERROR: {}".format(response.content.decode()))
                return jsonify({
                    "success": False,
                    "message": "Error invoking Lambda function",
                    "lambda_response": response.content.decode()
                })
    except Exception as e:
        logger.error('Exception occurred', exc_info=True)
        return jsonify({"success": False, "message": "An error occurred while processing the request"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)