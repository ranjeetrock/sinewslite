# sinewslite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.admin import create_temp_admin   

urlpatterns = [
    path('admin/', admin.site.urls),
     path("create-temp-admin/", create_temp_admin),  # 🚨 temporary URL
   path('', include('news.urls', namespace='news')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)