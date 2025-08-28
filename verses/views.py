import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema

from .models import Verse
from .serializers import VerseSerializer

OURMANNA_URL = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"

class VerseViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer
    lookup_field = "reference" 

    @extend_schema(responses=VerseSerializer)
    @action(detail=False, methods=["get"], url_path="today")
    def verse_of_the_day(self, request):
        today = now().date()
        verse = Verse.objects.filter(created_at__date=today).first()
        if verse:
            serializer = self.get_serializer(verse)
            return Response(serializer.data)

        response = requests.get(OURMANNA_URL)
        if response.status_code == 200:
            data = response.json()
            details = data["verse"]["details"]
            ref = details["reference"]
            text = details["text"]
            translation = details["version"]

            verse = Verse.objects.create(reference=ref, text=text, translation=translation)
            serializer = self.get_serializer(verse)
            return Response(serializer.data)

        return Response({"error": "Could not fetch verse"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(responses=VerseSerializer)
    @action(detail=False, methods=["get"], url_path="random")
    def random_verse(self, request):
        verse = Verse.objects.order_by("?").first()
        if not verse:
            return Response({"error": "No verses cached yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(verse)
        return Response(serializer.data)
