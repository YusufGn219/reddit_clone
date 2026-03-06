from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from posts.models import Post, Comment
from .services import toggle_post_vote, toggle_comment_vote


def _parse_value(raw: str):
    if raw == "up":
        return 1
    if raw == "down":
        return -1
    return None


@login_required
@require_POST
def vote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    value = _parse_value(request.POST.get("value"))
    if value is None:
        return HttpResponseBadRequest("Invalid vote value")

    toggle_post_vote(post=post, user=request.user, value=value)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
@require_POST
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    value = _parse_value(request.POST.get("value"))
    if value is None:
        return HttpResponseBadRequest("Invalid vote value")

    toggle_comment_vote(comment=comment, user=request.user, value=value)
    return redirect(request.META.get("HTTP_REFERER", "/"))
