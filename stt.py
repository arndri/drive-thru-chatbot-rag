import whisper
import numpy as np
import sounddevice as sd
import torch
import scipy.io.wavfile as wav
import tempfile
import pyuac
import os
import time

model = whisper.load_model("large")

# Set recording parameters
SAMPLE_RATE = 16000  # Whisper expects 16kHz audio
DURATION = 5  # Capture 5 seconds at a time
temp_dir = "D:/Project/speech-recognition/temp" 

def ensure_temp_dir():
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
    os.chmod(temp_dir, 0o777)

def record_and_transcribe():
    print("🎤 Listening... Speak now")

    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    temp_file = os.path.join(temp_dir, f"audio_{int(time.time())}.wav")
    try:
        wav.write(temp_file, SAMPLE_RATE, audio)
        result = model.transcribe(temp_file, language='indonesian')
        print("📝 Transcription:", result['text'])
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {e}")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        ensure_temp_dir()
        while True:
            record_and_transcribe()