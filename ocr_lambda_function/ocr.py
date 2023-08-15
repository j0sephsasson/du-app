import base64
import os
from datetime import datetime
from paddleocr import PaddleOCR
import json
from io import BytesIO

model = None
try:
    # set model paths
    det_model_path = "/app/models/.paddleocr/whl/det/ch/ch_PP-OCRv3_det_infer"
    rec_model_path = "/app/models/.paddleocr/whl/rec/ch/ch_PP-OCRv3_rec_infer"
    cls_model_path = "/app/models/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer"

    # init model
    model = PaddleOCR(use_angle_cls=True, use_gpu=False, 
                      det_model_dir=det_model_path, 
                      rec_model_dir=rec_model_path,
                      cls_model_dir=cls_model_path)
except Exception as e:
    print("Failed to initialize PaddleOCR: %s", str(e))

def ocr(path):
    if not model:
        print("PaddleOCR model is not initialized.")
        return None

    result = model.ocr(path, cls=True)
    ocr_strings = []  # Initialize an empty list
    
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            ocr_strings.append(line[1][0])  # append each string to the list

    return ocr_strings

def lambda_handler(event, context):
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

    ocr_strings = ocr(full_path)

    if ocr_strings:
        final = ' '.join(ocr_strings)

        response_body = {
            'ocr_result': final
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
    else:
        return {
            'statusCode': 500
        }