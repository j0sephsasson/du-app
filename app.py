from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session, current_app

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the main index page.

    Returns:
        str: Rendered index.html template.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)