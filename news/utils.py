import requests
from django.conf import settings

def get_breaking_news():
    try:
        print("Making request to NewsAPI...")
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "country": "in",  # You can also use 'us' or others for testing
                "apiKey": settings.NEWSAPI_KEY,
                "pageSize": 5
            },
            timeout=5
        )
        print("Status code:", response.status_code)
        print("Raw response:", response.text)

        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        else:
            print("Failed to fetch articles. Status code:", response.status_code)
            return []
    except Exception as e:
        print("Exception in get_breaking_news:", e)
        return []
