from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VerseViewSet

router = DefaultRouter()
router.register(r"", VerseViewSet, basename="verses")

urlpatterns = [
    path("", include(router.urls)),
]
