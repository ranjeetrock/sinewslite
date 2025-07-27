from django.contrib import admin
from .models import  PatrakaarMitra  # ✅ import only existing models



@admin.register(PatrakaarMitra)
class PatrakaarMitraAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mobile', 'email', 'category']
