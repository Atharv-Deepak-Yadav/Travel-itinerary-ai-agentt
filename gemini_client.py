# gemini_client.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)

def generate_text(prompt, model="gemini-2.0-flash"):
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"
