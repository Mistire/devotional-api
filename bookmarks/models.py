from django.conf import settings
from django.db import models
from devotionals.models import Devotional
from verses.models import Verse

# Create your models here.
class Bookmark(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="bookmarks"
  )
  verse = models.ForeignKey(
    Verse,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="bookmarks"
  )
  devotional = models.ForeignKey(
    Devotional,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="bookmarks"
  )
  created_at = models.DateField(auto_now_add=True)

  class Meta:
    unique_together = ("user", "verse", "devotional")

  def __str__(self):
    if self.verse:
      return f"{self.user.username} bookmarked verse {self.verse.reference}"
    if self.devotional:
      return f"{self.user.username} bookmarked devotional {self.devotional.title}"
    return f"{self.user.username} bookmark"
  