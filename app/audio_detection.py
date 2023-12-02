# audio_detection.py

import speech_recognition as sr
from pydub import AudioSegment
def detect_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio.export(file_path, format="wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile(file_path) as audio_file:
            audio_data = recognizer.record(audio_file)
            text = recognizer.recognize_google(audio_data)

        return text

    except Exception as e:
        # Handle exceptions, log errors, etc.
        print(f"Error processing audio: {e}")
        return None

