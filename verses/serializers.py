from rest_framework import serializers
from .models import Verse

class VerseSerializer(serializers.ModelSerializer):
  combined = serializers.SerializerMethodField()

  class Meta:
    model = Verse
    fields = ["id", "reference", "text", "translation", "combined"]

  def get_combined(self, obj):
    return f"{obj.reference} ({obj.translation}): {obj.text}"
