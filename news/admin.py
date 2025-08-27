from django.contrib import admin
from .models import  PatrakaarMitra  # ✅ import only existing models



@admin.register(PatrakaarMitra)
class PatrakaarMitraAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile', 'email', 'category']


    # ENewsPaper
from .models import ENewsPaper

@admin.register(ENewsPaper)
class ENewsPaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_on", "uploaded_by")
    search_fields = ("title", "uploaded_by")





# news/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_temp_admin(request):
    TEMP_USERNAME = "tempadmin"
    TEMP_EMAIL = "temp@domain.com"
    TEMP_PASSWORD = "TempPass123!"

    if not User.objects.filter(username=TEMP_USERNAME).exists():
        User.objects.create_superuser(
            username=TEMP_USERNAME,
            email=TEMP_EMAIL,
            password=TEMP_PASSWORD
        )
        return HttpResponse("✅ Temporary admin created successfully.")
    else:
        return HttpResponse("⚠️ Temporary admin already exists.")

# Register your models here as usual
