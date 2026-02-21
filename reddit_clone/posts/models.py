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

class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    body = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment({self.id})"