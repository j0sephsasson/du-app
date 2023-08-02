from flask import Flask, request, jsonify, g
from paddleocr import PaddleOCR, draw_ocr
import logging
from PIL import Image
import io
import os, shutil

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

model = PaddleOCR(use_angle_cls=True,use_gpu=False)

# Function to perform OCR
def ocr(path):
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

@app.route('/')
def index():
    # Log the received text
    logging.info('I was called')

    return 'Hello World!'

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'status': 'No file part in the request'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser might
    # submit an empty file without a filename.
    if file.filename == '':
        return jsonify({'status': 'No selected file'}), 400

    if file:
        filepath = os.path.join('/tmp', file.filename)
        file.save(filepath)

        # OCR and write to file
        string_list = ocr(filepath)

        return jsonify({'status': 'success', 'result':string_list}), 200

    return jsonify({'status': 'An error occurred processing the file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)