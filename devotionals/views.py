from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Devotional
from .serializers import DevotionalSerializer

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # public can see approved items; owners/admins can see their own unapproved
            return obj.is_approved or (request.user.is_authenticated and (obj.author_id == request.user.id or request.user.is_staff))
        return request.user.is_authenticated and (obj.author_id == request.user.id or request.user.is_staff)

@extend_schema(tags=["Devotionals"])
class DevotionalViewSet(viewsets.ModelViewSet):
    serializer_class = DevotionalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "tags", "author__username"]
    ordering_fields = ["date", "created_at"]

    def get_queryset(self):
        qs = Devotional.objects.all()
        user = self.request.user
        # Public sees only approved; owner/admin see their own/all respectively
        if not user.is_authenticated or not user.is_staff:
            if user.is_authenticated:
                return qs.filter(Q(is_approved=True) | Q(author=user))
            return qs.filter(is_approved=True)
        return qs

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        if self.action in ["approve", "feature", "unfeature"]:
            return [permissions.IsAdminUser()]
        return [IsOwnerOrAdminOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, is_approved=False)

    @extend_schema(tags=["Devotionals"], description="Get today's devotional (featured first, else latest approved for today).")
    @action(detail=False, methods=["get"], url_path="today", permission_classes=[permissions.AllowAny])
    def today(self, request):
        today_date = now().date()
        devo = (Devotional.objects.filter(date=today_date, is_approved=True, is_featured=True).first()
                or Devotional.objects.filter(date=today_date, is_approved=True).order_by("-created_at").first())
        if not devo:
            return Response({"detail": "No devotional for today."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(devo).data)

    @extend_schema(tags=["Devotionals"], description="Admin: approve a devotional.")
    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        devo = self.get_object()
        devo.is_approved = True
        devo.save()
        return Response({"status": "approved"})

    @extend_schema(tags=["Devotionals"], description="Admin: mark as featured.")
    @action(detail=True, methods=["post"], url_path="feature")
    def feature(self, request, pk=None):
        devo = self.get_object()
        devo.is_featured = True
        devo.save()
        return Response({"status": "featured"})

    @extend_schema(tags=["Devotionals"], description="Admin: remove featured flag.")
    @action(detail=True, methods=["post"], url_path="unfeature")
    def unfeature(self, request, pk=None):
        devo = self.get_object()
        devo.is_featured = False
        devo.save()
        return Response({"status": "unfeatured"})
