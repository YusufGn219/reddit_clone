from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class User(AbstractUser):
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

    def __str__(self):
        return f"{self.user.username} profile"


class Notification(models.Model):
    REPLY = "reply"
    TYPE_CHOICES = [(REPLY, "Reply")]

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
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user} - {self.type}"