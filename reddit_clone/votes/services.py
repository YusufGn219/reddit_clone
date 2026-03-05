from django.db import transaction
from django.db.models import Sum

from .models import PostVote, CommentVote


@transaction.atomic
def toggle_post_vote(*, post, user, value: int) -> int:
    obj = PostVote.objects.filter(post=post, user=user).first()

    if obj and obj.value == value:
        obj.delete()
    elif obj:
        obj.value = value
        obj.save(update_fields=["value"])
    else:
        PostVote.objects.create(post=post, user=user, value=value)

    return PostVote.objects.filter(post=post).aggregate(s=Sum("value"))["s"] or 0


@transaction.atomic
def toggle_comment_vote(*, comment, user, value: int) -> int:
    obj = CommentVote.objects.filter(comment=comment, user=user).first()

    if obj and obj.value == value:
        obj.delete()
    elif obj:
        obj.value = value
        obj.save(update_fields=["value"])
    else:
        CommentVote.objects.create(comment=comment, user=user, value=value)

    return CommentVote.objects.filter(comment=comment).aggregate(s=Sum("value"))["s"] or 0
    