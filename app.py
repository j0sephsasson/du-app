from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session, current_app
import time
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/joesasson/Desktop/sites/du/du-app/static/uploads'

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

    time.sleep(4)

    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected for uploading"})

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # At this point, you can process the file as you wish and then respond accordingly.
        return jsonify({"success": True, "message": "File successfully uploaded"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)