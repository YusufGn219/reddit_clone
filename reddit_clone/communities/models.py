from django.conf import settings
from django.db import models

class Community(models.Model):
    name = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete =models.CASCADE,
        related_name = "communities_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self) -> str:
        return f"c/{self.name}"