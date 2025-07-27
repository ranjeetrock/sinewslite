# news/context_processors.py
import requests
from django.conf import settings

def breaking_news(request):
    # print("Fetching breaking news...")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',  # ✅ Try 'us' instead of 'in'
        'category': 'general',  # ✅ Adding category improves results
        'pageSize': 5,
        'apiKey': settings.NEWS_API_KEY
    }

    try:
        # print("Making request to NewsAPI...")
        response = requests.get(url, params=params)
        # print("Status code:", response.status_code)
        data = response.json()
        # print("Fetched breaking articles:", data.get("articles", []))
        return {
            'breaking_news': data.get("articles", [])
        }
    except Exception as e:
        # print("Exception in get_breaking_news:", e)
        return {
            'breaking_news': []
        }
