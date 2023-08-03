import os
import requests
import base64
from io import BytesIO
import logging
from dotenv import load_dotenv
from datetime import datetime

# Get the current date and time
now = datetime.now()

# Convert the current date and time into a string format: 'Year-Month-Day_Hour-Minute-Second'
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Create a filename for log file
log_filename = f'logs/tasks_{date_time}.log'

# Configure the logging
logging.basicConfig(filename=log_filename, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('upload_task')

load_dotenv()

def process_upload(file_contents, filename):
    """
    Process uploaded PDF document

    Returns:
        str: Response message and success indication
    """
    try:
        logger.info(f'File "{filename}" received for uploading')

        # Prepare the request to the lambda URL
        api_url = os.getenv('LAMBDA_URL')
        file_ext = os.path.splitext(filename)[1]
        api_url += f"?file_ext={file_ext}"
        logger.info(f'Prepared API URL: {api_url}')

        file_obj = BytesIO(file_contents)

        # Send the request and get the response
        logger.info('Sending request to Lambda function')
        response = requests.post(api_url, files={"input_file": file_obj})

        # Process the response from Lambda function
        if response.status_code == 200:
            lambda_response = response.json()
            logger.info("SUCCESS: {}".format(lambda_response["ocr_result"]))
            return {
                "success": True,
                "message": "File successfully uploaded",
                "ocr_result": lambda_response["ocr_result"]
            }
        else:
            logger.error("ERROR: {}".format(response.content.decode()))
            return {
                "success": False,
                "message": "Error invoking Lambda function",
                "lambda_response": response.content.decode()
            }
    except Exception as e:
        logger.error('Exception occurred', exc_info=True)
        return {"success": False, "message": "An error occurred while processing the request"}
