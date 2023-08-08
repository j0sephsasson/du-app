import os
import requests
import base64
from urllib.parse import quote
from io import BytesIO
import logging
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

def call_llm(text, fields):
    """
    Creates vectorstore and query for fields

    Returns:
        dict: Final response and success indication
    """
    try:
        api_url = str(os.getenv('LAMBDA_URL_LLM'))

        # Properly encode parameters
        encoded_text = quote(text)
        encoded_fields = quote(fields)

        api_url += f"?text={encoded_text}&questions={encoded_fields}"

        response = requests.post(api_url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

        return {
            "success": True,
            "message": "Data successfully extracted",
            "fields": fields,
            "final_result": response.text
        }

    except requests.ConnectionError:
        logging.error("Failed to connect to the API")
        return {
            "success": False,
            "message": "Failed to connect to the API",
            "final_result": None
        }

    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        return {
            "success": False,
            "message": f"HTTP error occurred: {e}",
            "final_result": None
        }

    except Exception as e:  
        logging.error(f"An error occurred: {e}")
        return {
            "success": False,
            "message": f"An error occurred: {e}",
            "final_result": None
        }

def process_upload(file_contents, filename, fields):
    """
    Process uploaded PDF document (performs OCR)

    Returns:
        dict: Response message and success indication
    """
    try:
        logging.info(f'File "{filename}" received for uploading')

        # Prepare the request to the lambda URL
        api_url = os.getenv('LAMBDA_URL_OCR')
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
            logging.info("OCR SUCCESS")
            final_result = call_llm(text=str(lambda_response["ocr_result"]), fields=fields)
            return final_result
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
