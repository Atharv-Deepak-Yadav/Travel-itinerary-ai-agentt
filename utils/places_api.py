# utils/places_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def nearby_search(location: str, query: str):
    if not API_KEY:
        return None

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"{query} in {location}", "key": API_KEY}
    return requests.get(url, params=params).json()
