import requests

API_KEY = ""

def fetch_news(query):
    url = "http://api.mediastack.com/v1/news"

    params = {
        "access_key": API_KEY,
        "keywords": query,
        "languages": "en",
        "limit": 5
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
