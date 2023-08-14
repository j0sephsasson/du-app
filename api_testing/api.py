import requests, json, os
from io import BytesIO
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

def send_to_ocr_api(file_path):
    api_url = os.getenv("LAMBDA_OCR_API")

    # Read the PDF file and convert its content into bytes
    with open(file_path, 'rb') as f:
        byte_content = BytesIO(f.read())

    # This is a generic example to send the byte content to an API
    # Adjust this based on the specifics of your API
    response = requests.post(api_url, files={'input_file': byte_content})

    return response.json()  # Assuming the API returns a JSON response

def send_to_llm_api(text, fields):
    api_url = os.getenv('LAMBDA_URL_LLM')

    # Prepare payload to be sent in the body
    payload = {
        'text': text,
        'questions': fields
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # Use data parameter to send payload as json
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    return response.json()


if __name__ == '__main__':
    file_path = '/Users/joesasson/Desktop/invoice.pdf'
    fields = 'Total, Invoice number'

    result = send_to_ocr_api(file_path)
    ocr_result = result['ocr_result']

    print('OCR SUCCESS')

    final = send_to_llm_api(ocr_result, fields)

    print(final)
