import whisper
import numpy as np

model = whisper.load_model("large")
result = model.transcribe("test.mp3",language='indonesian', vad=True)
print(result['text'])