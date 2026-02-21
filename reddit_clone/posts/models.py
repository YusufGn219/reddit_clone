from django.db import models
from django.conf import settings
from communities.models import Community

class Post(models.Model):
    community = models.ForeignKey (
        Community,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    author = models.ForeignKey (
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.author.username}"