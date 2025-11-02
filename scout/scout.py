# aivpn/scout/scout.py
import requests
from typing import List, Dict

TMDB_KEY = "YOUR_TMDB_KEY"
GEMINI_KEY = "YOUR_GEMINI_KEY"

def search_free_streams(title: str) -> List[Dict]:
    # 1. Search TMDB
    tmdb = requests.get(
        f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_KEY}&query={title}"
    ).json()
    
    if not tmdb["results"]:
        return []
    
    # 2. Ask Gemini: "In which countries is [title] free to stream legally?"
    prompt = f"""
    List countries where "{title}" is legally free to stream (YouTube, public TV, etc.).
    Format: COUNTRY: SERVICE
    """
    gemini = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers={"x-goog-api-key": GEMINI_KEY},
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    ).json()
    
    countries = []
    try:
        text = gemini["candidates"][0]["content"]["parts"][0]["text"]
        for line in text.split("\n"):
            if ":" in line:
                country, service = line.split(":", 1)
                countries.append({"country": country.strip(), "service": service.strip(), "free": True})
    except:
        pass
    
    return countries

# Example
if __name__ == "__main__":
    print(search_free_streams("The Office"))
