from make_db import MenuDB
from speech_processor import SpeechProcessor
from order_processor import OrderProcessor
from llm_parser import LLMParser

def main():
    db = MenuDB()
    speech = SpeechProcessor()
    llm_parser = LLMParser()
    order_processor = OrderProcessor(db, llm_parser)

    # Add menu only once
    db.add_item("Burger", 5.99, 10)
    db.add_item("Kentang", 2.99, 15)
    db.add_item("Coca-Cola", 1.99, 20)

    audio_file = "test.mp3"
    try:
        transcription = speech.transcribe(audio_file)
        order_processor.process_order(transcription)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()