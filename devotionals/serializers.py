from rest_framework import serializers
from .models import Devotional
from datetime import date

class DevotionalSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Devotional
        fields = [
            "id","title","content","author","author_name",
            "tags","date","is_approved","is_featured",
            "created_at","updated_at",
        ]
        read_only_fields = ["author","is_approved","is_featured","created_at","updated_at"]

    def validate_date(self, value):
      if value > date.today(): raise serializers.ValidationError("Date cannot be in the future.")
      return value
