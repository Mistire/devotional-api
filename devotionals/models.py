from django.db import models
from django.conf import settings

class Devotional(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devotionals"
    )
    tags = models.CharField(max_length=255, blank=True)
    date = models.DateField() 
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.date})"
