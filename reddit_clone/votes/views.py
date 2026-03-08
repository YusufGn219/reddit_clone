from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from posts.models import Post, Comment
from .services import toggle_post_vote, toggle_comment_vote
from .models import PostVote, CommentVote


def _parse_value(raw: str):
    if raw == "up":
        return 1
    if raw == "down":
        return -1
    return None


def _get_user_vote(vote_model, filter_kwargs):
    obj = vote_model.objects.filter(**filter_kwargs).first()
    return obj.value if obj else 0


@login_required
@require_POST
def vote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    value = _parse_value(request.POST.get("value"))
    if value is None:
        return JsonResponse({"error": "Invalid vote value"}, status=400)

    new_score = toggle_post_vote(post=post, user=request.user, value=value)
    user_vote = _get_user_vote(PostVote, {"post": post, "user": request.user})

    return JsonResponse({"score": new_score, "user_vote": user_vote})


@login_required
@require_POST
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    value = _parse_value(request.POST.get("value"))
    if value is None:
        return JsonResponse({"error": "Invalid vote value"}, status=400)

    new_score = toggle_comment_vote(comment=comment, user=request.user, value=value)
    user_vote = _get_user_vote(CommentVote, {"comment": comment, "user": request.user})

    return JsonResponse({"score": new_score, "user_vote": user_vote})