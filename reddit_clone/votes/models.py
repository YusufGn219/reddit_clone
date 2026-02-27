from django.conf import settings
from django.db import models


class PostVote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES=(
        (UP , "Upvote"),
        (DOWN, "Downvote")
    )

    post = models.ForeignKey("posts.Post", on_delete = models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="post_votes")
    value = models.IntegerField(choices=VALUE_CHOICES)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="uniq_post_vote_per_user")
        ]


class CommentVote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "Upvote"),
        (DOWN, "Downvote"),
    )

    comment = models.ForeignKey("posts.Comment", on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_votes")
    value = models.SmallIntegerField(choices=VALUE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["comment", "user"], name="uniq_comment_vote_per_user")
        ]
