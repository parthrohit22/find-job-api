import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
    raise RuntimeError("RapidAPI configuration missing: RAPIDAPI_KEY or RAPIDAPI_HOST not set")