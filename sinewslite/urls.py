# sinewslite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.views import create_admin_user


urlpatterns = [
    path('admin/', admin.site.urls),
   path('', include('news.urls', namespace='news')),
   path('create-admin-user/', create_admin_user),  # 👈 Temporary URL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)