from rest_framework.routers import DefaultRouter
from .views import DevotionalViewSet

router = DefaultRouter()
router.register(r"", DevotionalViewSet, basename="devotional")
urlpatterns = router.urls
