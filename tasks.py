import os
import requests
import base64
from io import BytesIO
import logging
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

def process_upload(file_contents, filename):
    """
    Process uploaded PDF document

    Returns:
        str: Response message and success indication
    """
    try:
        logging.info(f'File "{filename}" received for uploading')

        # Prepare the request to the lambda URL
        api_url = os.getenv('LAMBDA_URL')
        file_ext = os.path.splitext(filename)[1]
        api_url += f"?file_ext={file_ext}"
        logging.info(f'Prepared API URL: {api_url}')

        file_obj = BytesIO(file_contents)

        # Send the request and get the response
        logging.info('Sending request to Lambda function')
        response = requests.post(api_url, files={"input_file": file_obj})

        # Process the response from Lambda function
        if response.status_code == 200:
            lambda_response = response.json()
            logging.info("SUCCESS: {}".format(lambda_response["ocr_result"]))
            return {
                "success": True,
                "message": "File successfully uploaded",
                "ocr_result": lambda_response["ocr_result"]
            }
        else:
            logging.error("ERROR: {}".format(response.content.decode()))
            return {
                "success": False,
                "message": "Error invoking Lambda function",
                "lambda_response": response.content.decode()
            }
    except Exception as e:
        logging.error('Exception occurred', exc_info=True)
        return {"success": False, "message": "An error occurred while processing the request"}
