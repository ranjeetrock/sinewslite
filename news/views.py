import requests
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
# from news.models import Category 
from django.shortcuts   import render, redirect
from django.shortcuts import render
from .forms import PatrakaarMitraForm
from .forms import PatrakaarMitra
import pytz  # pip install pytz if not available

def fetch_news(*, country="in", category=None, page_size=50):
    api_key = getattr(settings, "NEWS_API_KEY", None)

    if not api_key:
        return [], "API key not found"

    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "pageSize": page_size,
    }

    if category:
        params["category"] = category

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        articles = data.get("articles", [])

        if not articles and country == "in":
            params["country"] = "us"
            response = requests.get(base_url, params=params)
            data = response.json()
            articles = data.get("articles", [])

        # ✅ Add IST conversion here
        for article in articles:
            if article.get("publishedAt"):
                article["published_at_ist"] = convert_utc_to_ist(article["publishedAt"])
                # print(article['published_at_ist'])

            else:
                article["published_at_ist"] = "N/A"

        return articles, None if articles else "No articles returned from NewsAPI"
    except Exception as e:
        return [], str(e)
    
    
def frontpage(request):
    articles, error = fetch_news()
    paginator = Paginator(articles, 12)
    page_number = request.GET.get("page", 1)


   

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({"has_next": False, "html": ""})

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render(request, "news/_article_cards.html", {"page_obj": page_obj}).content.decode("utf-8")
        return JsonResponse({"has_next": page_obj.has_next(), "html": html})

    return render(request, "news/frontpage.html", {
        "page_obj": page_obj,
        "live_error": error,
        "now": datetime.now()
    })


# ✅ View for live category (from NewsAPI)
def live_category(request, category_slug):
    articles, live_error = fetch_news(country="in", category=category_slug, page_size=50)
    if not articles:
        articles, live_error = fetch_news(country="us", category=category_slug, page_size=50)
    paginator = Paginator(articles, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    category_name = category_slug.capitalize()
# ....
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({"has_next": False, "html": ""})

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render(request, "news/_article_cards.html", {"page_obj": page_obj}).content.decode("utf-8")
        return JsonResponse({"has_next": page_obj.has_next(), "html": html})
# .....
    # if request.headers.get("x-requested-with") == "XMLHttpRequest":
    #     return render(request, "news/_article_cards.html", {"page_obj": page_obj})

    return render(request, "news/live_category.html", {
        "page_obj": page_obj,
        # "live_news": articles,
        "live_error": live_error,
        "category": category_slug.capitalize(),
        "now": datetime.now(),
    })



def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(category=category).order_by("-created_at")
    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"has_next": False, "html": ""})
        page_obj = paginator.page(1)

    # Handle AJAX (infinite scroll)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render(request, "news/_article_cards.html", {"page_obj": page_obj}).content.decode("utf-8")
        return JsonResponse({"has_next": page_obj.has_next(), "html": html})

    return render(request, "news/category.html", {
        "category": category,
        "page_obj": page_obj
    })





def register_view(request):
    if request.method == 'POST':
        form = PatrakaarMitraForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'news/registration_success.html')
        else:
            return render(request, 'news/patrakaar_register.html', {'form': form})
    else:
        form = PatrakaarMitraForm()
    return render(request, 'news/patrakaar_register.html', {'form': form})







def live_category_view(request, category):
    page = int(request.GET.get("page", 1))
    articles, has_next, error = fetch_live_news(category=category, page=page)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("news/_article_cards.html", {"page_obj": articles})
        return JsonResponse({"has_next": has_next, "html": html})

    return render(request, "news/live_category.html", {
        "category": category,
        "page_obj": articles,
        "live_error": error
    })


def search_view(request):
    query = request.GET.get("q", "").strip()
    api_key = getattr(settings, "NEWS_API_KEY", None)
    articles = []
    error = None

    if query and api_key:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": api_key,
                "pageSize": 50,
                "language": "en",
                "sortBy": "publishedAt"
            }
            response = requests.get(url, params=params)
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
            else:
                error = data.get("message", "Unknown error from NewsAPI")
        except Exception as e:
            error = str(e)

    # Paginate articles
    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"has_next": False, "html": ""})
        page_obj = paginator.page(1)

    # Handle AJAX scroll
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render(request, "news/_article_cards.html", {"page_obj": page_obj}).content.decode("utf-8")
        return JsonResponse({"has_next": page_obj.has_next(), "html": html})

    return render(request, "news/search.html", {
        "query": query,
        "page_obj": page_obj,
        "live_error": error,
        "now": datetime.now()
    })

# Breaking News

from django.shortcuts import render
from .api_utils import get_breaking_news

def home(request):
    breaking_news = get_breaking_news()
    print("Fetched News:", breaking_news)  # This will show in terminal
    return render(request, 'news/home.html', {'breaking_news': breaking_news})






import requests
from django.conf import settings

def get_breaking_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',  # India, change if needed
        'apiKey': settings.NEWS_API_KEY,
        'pageSize': 5,  # Number of headlines to show
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('articles', [])
    except Exception as e:
        # print("Error fetching news:", e)
        return []




# time stamp


def convert_utc_to_ist(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')  # NewsAPI format
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = utc_time.astimezone(ist)
    return ist_time.strftime('%d %b %Y, %I:%M %p')  # Example: 26 Jul 2025, 04:15 PM



from .models import ENewsPaper
from django.shortcuts import render

def enews_page(request):
    papers_all = ENewsPaper.objects.all()
    return render(request, "_sidebar.html", {"papers_all": papers_all})
