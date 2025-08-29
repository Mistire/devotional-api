from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "user", "verse", "devotional", "created_at"]
        read_only_fields = ["user", "created_at"]
