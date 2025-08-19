# news/urls.py
from django.urls import path
from . import views
# from .views import frontpage, live_category, patrakaar_register_view  # , article_detail
from django.contrib.auth import views as auth_views
from .views import register_view



app_name = 'news'

urlpatterns = [
   
     path("", views.frontpage, name="frontpage"),
    
     path("category/<slug:category_slug>/", views.live_category, name="live_category"),
     path('search/', views.search_view, name='search'),
     path('register/', register_view, name='register'),
     path('login/', auth_views.LoginView.as_view(template_name='news/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
     path("e-news/", views.enews_page, name="enews_list"),


]










