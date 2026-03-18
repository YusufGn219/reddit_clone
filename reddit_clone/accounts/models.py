from enum import unique
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
import uuid


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)  # ← class içinde, property dışında

    @property
    def karma(self):
        from votes.models import PostVote, CommentVote

        post_karma = PostVote.objects.filter(
            post__author=self
        ).aggregate(total=Sum("value"))["total"] or 0

        comment_karma = CommentVote.objects.filter(
            comment__author=self
        ).aggregate(total=Sum("value"))["total"] or 0

        return post_karma + comment_karma

    @property
    def karma(self):
       
        from votes.models import PostVote, CommentVote

        post_karma = PostVote.objects.filter(
            post__author=self
        ).aggregate(total=Sum("value"))["total"] or 0

        comment_karma = CommentVote.objects.filter(
            comment__author=self
        ).aggregate(total=Sum("value"))["total"] or 0
       
        return post_karma + comment_karma


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)
    display_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"


class Notification(models.Model):
    REPLY = "reply"
    AWARD = "award"
    FOLLOW = "follow"
    TYPE_CHOICES = [
        (REPLY, "Reply"),
        (AWARD, "Award"),
        (FOLLOW, "Follow"),
    ]

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=REPLY)
    comment = models.ForeignKey(
        "posts.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    actor = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user} - {self.type}"

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user} - {self.type}"
        
class EmailVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_token"
    )
    token = models.UUIDField(default=uuid.uuid4, unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Token for {self.user.username}"
    
class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followed=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
