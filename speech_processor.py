import os
import whisper

class SpeechProcessor:
    def __init__(self, model_size="large"):
        print("🔊 Loading Whisper model...")
        self.model = whisper.load_model(model_size)

    def transcribe(self, file_path, language='indonesian'):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        print(f"🎧 Transcribing {file_path}...")
        result = self.model.transcribe(file_path, language=language)
        print("📝 Transcription result:", result['text'])
        return result['text']
