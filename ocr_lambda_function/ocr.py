import logging
import base64
import os
from datetime import datetime
import traceback

try:
    from paddleocr import PaddleOCR
except Exception as e:
    logging.error("Exception occurred during import: %s", str(e))
    logging.error(str(traceback.format_exc()))
import json
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)

def ocr(path):
    # Initialize the model
    try:
        model = PaddleOCR(use_angle_cls=True, use_gpu=False)
    except Exception as e:
        logging.info("Exception occurred: %s", str(e))
        logging.info(str(traceback.format_exc()))
        return None

    
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
    logging.info("lambda function invoked")

    # Use the file extension in the input_key
    file_ext = event["queryStringParameters"]["file_ext"]
    

    # Create the filename and the directories
    input_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}{file_ext}'
    input_directory = 'sourcedata'
    full_path = f'/tmp/{input_directory}/{input_filename}'

    # Create directories until the penultimate level
    os.makedirs(f'/tmp/{input_directory}', exist_ok=True)
    
    # Use BytesIO to handle both text and binary file types
    input_content = BytesIO(base64.b64decode(event['body']))

    # Write your file to the leaf level
    with open(full_path, 'wb') as f:
        f.write(input_content.read())

    logging.info("file saved...performing OCR next")

    ocr_strings = ocr(full_path)

    if ocr_strings:

        response_body = {
            'ocr_result': ocr_strings
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
    else:
        return {
            'statusCode': 500
        }