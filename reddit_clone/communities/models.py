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
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self) -> str:
        return f"c/{self.name}"

class CommunityModerator(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete = models.CASCADE,
        related_name = "moderators"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "moderated_communities"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("community", "user")]

    def __str__(self):
        return f"{self.user} mod of {self.community}"

class CommunityRule(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="rules"
    )
    title= models.CharField(max_length=100)
    description = models.TextField(blank = True)
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.community.name} - {self.title}"

class BannedUser(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="bans")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bans")
    banned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issued_bans")
    reason = models.TextField(blank=True)
    banned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("community", "user")]

    def __str__(self):
        return f"{self.user} banned from {self.community}"

class CommunityMember(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="joined_communities"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =[("community","user")]

    def __str__(self):
        return f"{self.user} joined {self.community}"