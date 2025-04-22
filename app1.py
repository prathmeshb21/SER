import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from notebooks import main

app = Flask(__name__, template_folder='templates')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'run_data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('select1.html')

@app.route('/success', methods=['POST'])
def success():
    audio_file = request.files.get('audio_file')
    if not audio_file:
        return "No audio file uploaded", 400

    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(file_path)

    pred_output = main.process_files(str(file_path))
    return render_template("result.html", LABEL=pred_output)

if __name__ == '__main__':
    app.run(debug=True)
