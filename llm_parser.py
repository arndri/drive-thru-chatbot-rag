from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import json
import torch

class LLMParser:
    def __init__(self):
        print("🤖 Loading advanced LLM parser (Nous Hermes)...")
        model_name = "NousResearch/Nous-Hermes-2-Mistral-7B"
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def parse(self, transcript):
        prompt = f"""
Tolong ekstrak pesanan dari kalimat berikut dan ubah menjadi format JSON:

Kalimat: "{transcript}"

Format JSON yang diinginkan:
[
  {{ "item": "Burger", "quantity": 1 }},
  {{ "item": "Kentang", "quantity": 2 }}
]

Jawaban:
"""
        response = self.pipe(prompt, max_new_tokens=200, do_sample=False, temperature=0.3)
        generated_text = response[0]['generated_text']
        print("🧠 LLM raw response:", generated_text)

        # Try extracting JSON from the response
        try:
            json_start = generated_text.index("[")
            json_str = generated_text[json_start:]
            parsed = json.loads(json_str)
        except Exception as e:
            print(f"❌ Failed to parse order with LLM: {e}")
            parsed = []

        return parsed
