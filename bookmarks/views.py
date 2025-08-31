from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework import viewsets, status, permissions

from devotionals.models import Devotional
from verses.models import Verse
from .models import Bookmark
from .serializers import BookmarkSerializer
from verses.serializers import VerseSerializer
from devotionals.serializers import DevotionalSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated("You must be logged in to access bookmarks.")
        return Bookmark.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="verses")
    def verse_bookmarks(self, request):
        verse_bookmarks = self.get_queryset().filter(verse__isnull=False)
        serializer = BookmarkSerializer(verse_bookmarks, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="devotionals")
    def devotional_bookmarks(self, request):
        devo_bookmarks = self.get_queryset().filter(devotional__isnull=False)
        serializer = BookmarkSerializer(devo_bookmarks, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="details")
    def bookmark_details(self, request, pk=None):
        bookmark = self.get_object()

        if bookmark.verse:
            serializer = VerseSerializer(bookmark.verse, context={"request": request})
        elif bookmark.devotional:
            serializer = DevotionalSerializer(bookmark.devotional, context={"request": request})
        else:
            return Response(
                {"error": "Unsupported bookmark type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data)
