from flask import Flask, request, send_file, jsonify
import os
import uuid
from datetime import datetime
import json

app = Flask(__name__)

REMINDERS_FILE = "reminders.json"
AUDIO_FOLDER = "audio"

# Make sure folders exist
os.makedirs(AUDIO_FOLDER, exist_ok=True)
if not os.path.exists(REMINDERS_FILE):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return "Loyal Alarm Server is running."

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio = request.files['audio']
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(AUDIO_FOLDER, filename)
    audio.save(filepath)

    # ✨ MOCK STT and AI logic (you'll replace this with real processing)
    reminder_time = "07:00"
    message = "Feed the germs"
    
    response_filename = create_reminder_audio(message)
    save_reminder(message, reminder_time, response_filename)

    return jsonify({"response": response_filename})

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_file(os.path.join(AUDIO_FOLDER, filename), mimetype='audio/mpeg')

def create_reminder_audio(message):
    # For now, just simulate MP3 generation
    fake_mp3 = os.path.join(AUDIO_FOLDER, f"{uuid.uuid4()}.mp3")
    with open(fake_mp3, 'wb') as f:
        f.write(b"FAKE_MP3_CONTENT")
    return os.path.basename(fake_mp3)

def save_reminder(message, time, filename):
    with open(REMINDERS_FILE, 'r+') as f:
        reminders = json.load(f)
        reminders.append({
            "message": message,
            "time": time,
            "file": filename
        })
        f.seek(0)
        json.dump(reminders, f, indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
