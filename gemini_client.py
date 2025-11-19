# gemini_client.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)

def generate_text(prompt, max_output_tokens=512, model="models/gemini-pro-latest"):
    response = client.models.generate_content(
        model=model,
        contents=[prompt]
    )
    return response.text
