from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session, current_app
import time
from werkzeug.utils import secure_filename
import os
import requests
from io import BytesIO
from dotenv import load_dotenv
import base64

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

    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"})

    file = request.files['file']
    fields = request.form['fields']

    print('I was called')
    print('fields:', fields)

    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected for uploading"})

    if file:
        filename = secure_filename(file.filename)

        # Prepare the request to your API Gateway
        api_url = (os.getenv('LAMBDA_URL'))
        file_ext = os.path.splitext(filename)[1]
        api_url += f"?file_ext={file_ext}"

        headers = {
            "x-api-key": str(os.getenv('API_GATEWAY_KEY'))
        }

        file_obj = BytesIO(file.read())
        encoded_file = base64.b64encode(file_obj.getvalue()).decode()

        # Send the request and get the response
        response = requests.post(api_url, headers=headers, json={"body": encoded_file})

        # Process the response from your Lambda function
        if response.status_code == 200:
            lambda_response = response.json()
            print("SUCCESS:")
            print(lambda_response["ocr_result"])
            return jsonify({
                "success": True,
                "message": "File successfully uploaded",
                "ocr_result": lambda_response["ocr_result"]
            })
        else:
            print("ERROR:")
            print(response.content.decode())
            return jsonify({
                "success": False,
                "message": "Error invoking Lambda function",
                "lambda_response": response.content.decode()
            })


if __name__ == '__main__':
    app.run(debug=True, port=5000)