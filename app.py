from flask import Flask, request, jsonify,render_template
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_text = recognizer.record(source)
            text = recognizer.recognize_google(audio_text)
            return text
    except UnknownValueError:
        return "Speech not recognized"
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract audio from the video
        video_clip = VideoFileClip(filepath)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
        video_clip.audio.write_audiofile(audio_path)

        # Extract text from the audio
        text = extract_text_from_audio(audio_path)

        # Optionally, you can remove the uploaded files if needed
        # os.remove(filepath)
        # os.remove(audio_path)

        return jsonify({'text': text})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
