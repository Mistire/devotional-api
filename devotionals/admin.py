from django.contrib import admin
from .models import Devotional

@admin.register(Devotional)
class DevotionalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "date", "is_approved", "is_featured", "created_at")
    list_filter = ("is_approved", "is_featured", "date")
    search_fields = ("title", "content", "tags", "author__username", "author__email")
