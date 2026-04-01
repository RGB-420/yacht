import requests
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

def search_google(query, location):
    if not API_KEY:
        raise ValueError("SERPAPI_KEY not found in environment variables")
    
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": 10
    }

    if location:
        params["location"] = location

    print(f"\n Query: {query}")
    print(f" Location: {location}")

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    data = response.json()

    if "error" in data:
        raise Exception(f"SERPAPI error: {data['error']}")
    
    return data

def extract_organic_results(response_json):
    results = []

    for r in response_json.get("organic_results", []):
        results.append({
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet":r.get("snippet", "")
        })

    return results