import requests
from django.conf import settings

def get_breaking_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'in',
        'apiKey': settings.NEWS_API_KEY,
        'pageSize': 5,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('articles', [])
    except Exception as e:
        print("Error fetching news:", e)
        return []
