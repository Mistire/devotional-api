from django.db import models

# Create your models here.
class Verse(models.Model):
  reference = models.CharField(max_length=100, unique=True)
  text = models.TextField()
  translation = models.CharField(max_length=50, default="WEB")
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.reference} {self.translation}: {self.text}"