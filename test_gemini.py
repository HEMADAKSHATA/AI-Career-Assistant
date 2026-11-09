import os
from dotenv import load_dotenv

load_dotenv()
print("AI Career Assistant configuration test")
print("--------------------------------------")
print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("GEMINI_MODEL:", os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"))
print("No Gemini API request was sent.")
