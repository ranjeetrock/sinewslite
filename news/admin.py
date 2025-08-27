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
