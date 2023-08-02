import logging
import base64
import os
from datetime import datetime
from paddleocr import PaddleOCR
import json
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)

def ocr(path):
    # Initialize the model
    model = PaddleOCR(use_angle_cls=True,use_gpu=False)
    
    # Perform OCR
    logging.info("DOING OCR")

    result = model.ocr(path, cls=True)
    ocr_strings = []  # Initialize an empty list
    
    logging.info("LOOPING OVER RESULT")
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            ocr_strings.append(line[1][0])  # append each string to the list

    return ocr_strings

def lambda_handler(event, context):
    # Use the file extension in the input_key
    file_ext = event["queryStringParameters"]["file_ext"]
    input_key = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}{file_ext}'

    input_directory = f'sourcedata/{input_key}'
    
    # Use BytesIO to handle both text and binary file types
    input_content = BytesIO(base64.b64decode(event['body']))
    os.makedirs(f'/tmp/{input_directory}', exist_ok=True)
    with open(f'/tmp/{input_directory}', 'wb') as f:
        f.write(input_content.read())

    ocr_strings = ocr(f'/tmp/{input_directory}')

    response_body = {
        'ocr_result': ocr_strings
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }