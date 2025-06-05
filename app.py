import os, datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, url_for, redirect
from notebooks import main
from recommendations import SONG_RECOMMENDATIONS
import random
import numpy as np
app = Flask(__name__,template_folder='templates')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'run_data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('select2.html')

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
    #     tf = request.files['transcript_file']
        af = request.files['audio_file']
    #     tf_filename = secure_filename(tf.filename)
        af_filename = secure_filename(af.filename)
        print(af_filename)
    #     TRANS_FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], tf_filename)
        AUDIO_FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], af_filename)
    #     app.config['TRANS_FILE_PATH'] = TRANS_FILE_PATH
        app.config['AUDIO_FILE_PATH'] = AUDIO_FILE_PATH
    #     tf.save(app.config['TRANS_FILE_PATH'])
        af.save(app.config['AUDIO_FILE_PATH'])

        print(app.config['AUDIO_FILE_PATH'])
    #     print(app.config['TRANS_FILE_PATH'])
        pred_output = main.process_files(str(AUDIO_FILE_PATH))

        # After getting prediction
        #pred_output = main.process_files(str(AUDIO_FILE_PATH))

        # Example recommendation block
        #SONG_RECOMMENDATIONS = {
         #   "happy": [
          #      {"title": "Happy", "artist": "Pharrell Williams", "url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH"},
           #     {"title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "url": "https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc"},
            #],
            #"sad": [
            #    {"title": "Someone Like You", "artist": "Adele", "url": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"},
            #    {"title": "All of Me", "artist": "John Legend", "url": "https://open.spotify.com/track/3U4isOIWM3VvDubwSI3y7a"},
            #],
    # more emotions...
        #}

        all_songs = sum(SONG_RECOMMENDATIONS.values(), [])
        recommended_songs = random.sample(all_songs, 3) if len(all_songs) >= 3 else all_songs

        return render_template("result3.html", LABEL=pred_output, songs=recommended_songs)


 #   return render_template("result.html",LABEL=pred_output)
    # return 0


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
