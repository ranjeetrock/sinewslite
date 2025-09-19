
from django.contrib import admin
from .models import  PatrakaarMitra  # ✅ import only existing models

# Change header and title
admin.site.site_header = "SinewsLite Admin Panel"
admin.site.site_title = "SinewsLite Admin"
admin.site.index_title = "Welcome to SinewsLite"


@admin.register(PatrakaarMitra)
class PatrakaarMitraAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile', 'email', 'category']


    # ENewsPaper
from .models import ENewsPaper

@admin.register(ENewsPaper)
class ENewsPaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_on", "uploaded_by")
    search_fields = ("title", "uploaded_by")





