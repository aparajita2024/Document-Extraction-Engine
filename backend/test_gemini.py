# backend/test_gemini.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# List all available models
print("=== Available Models ===")
for model in client.models.list():
    print(model.name)

# Test a simple call
print("\n=== Testing API Call ===")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello in one word"
    )
    print("SUCCESS:", response.text)
except Exception as e:
    print("FAILED:", e)