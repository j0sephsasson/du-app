import requests
import json
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def send_to_ocr_api(file_path):
    """
    Send file to OCR API and return its response.
    
    Parameters:
    - file_path (str): Path to the file to be processed by the OCR.
    
    Returns:
    - dict: Response from the OCR API.
    
    Raises:
    - ValueError: If the API URL environment variable is missing or the request fails.
    """
    api_url = os.getenv("LAMBDA_OCR_API")

    # Validate if api_url is present
    if not api_url:
        raise ValueError("LAMBDA_OCR_API is missing in environment variables.")

    with open(file_path, 'rb') as f:
        byte_content = BytesIO(f.read())

    try:
        response = requests.post(api_url, files={'input_file': byte_content})
        response.raise_for_status()  # Will raise HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")

def send_to_llm_api(text, fields):
    """
    Send text and fields to LLM API and return its response.
    
    Parameters:
    - text (str): Text to be processed by the LLM API.
    - fields (str): Fields associated with the text.
    
    Returns:
    - dict: Response from the LLM API.
    
    Raises:
    - ValueError: If the API URL environment variable is missing or the request fails.
    """
    api_url = os.getenv('LAMBDA_URL_LLM')

    # Validate if api_url is present
    if not api_url:
        raise ValueError("LAMBDA_URL_LLM is missing in environment variables.")

    payload = {'text': text, 'questions': fields}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")