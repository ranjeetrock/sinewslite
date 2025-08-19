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



# news/context_processors.py
from .models import ENewsPaper

def enews_papers(request):
    """
    Return latest 5 ENewsPaper objects for sidebar.
    Keep this file simple and single-purpose.
    """
    papers = ENewsPaper.objects.all().order_by('-published_on')[:5]
    # temporary debug log that will appear in runserver console when a page renders
    print("context processor: found", papers.count(), "papers")
    return {"papers": papers}

