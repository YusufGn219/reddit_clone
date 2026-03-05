from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Comment
from .forms import PostCreateForm, CommentForm
from .services.comments import build_comment_tree
from django.db.models import Sum
from .services.querysets import with_post_score
from votes.models import CommentVote
from .services.sorting import normalize_sort_and_time, apply_sort
from communities.permissions import can_moderate
from django.db.models import Q
from communities.models import Community


def home_feed(request):
    sort, t = normalize_sort_and_time(request.GET)
    qs = Post.objects.filter(is_deleted=False).select_related("community", "author")
    qs = apply_sort(qs, sort, t)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/home_feed.html", {
        "page_obj": page_obj,
        "sort": sort,
        "t": t,
    })

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # ✅ namespace'li detail
            return redirect("posts:detail", post_id=post.id)
    else:
        form = PostCreateForm()

    return render(request, "posts/post_create.html", {"form": form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comment_form = CommentForm()
    comment_tree = build_comment_tree(post)

    if request.user.is_authenticated:
        vote_map = dict(
            CommentVote.objects
            .filter(user=request.user, comment__post=post)
            .values_list("comment_id", "value")
        )

        def attach_flags(nodes):
            for n in nodes:
                v = vote_map.get(n.id)
                n.is_upvoted = (v == 1)
                n.is_downvoted = (v == -1)
                attach_flags(getattr(n, "child_nodes", []))

        attach_flags(comment_tree)        

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
        "comment_tree": comment_tree,
    })


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method != "POST":
        return redirect("posts:detail", post_id=post.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.author = request.user
        c.parent = None
        c.post = post
        c.save()

    return redirect("posts:detail", post_id=post.id)


@login_required
def reply_create(request, post_id, parent_id):
    post = get_object_or_404(Post, pk=post_id)
    parent = get_object_or_404(Comment, pk=parent_id, post=post)

    if request.method != "POST":
        return redirect("posts:detail", post_id=post.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        r = form.save(commit=False)
        r.author = request.user
        r.parent = parent
        r.post = post
        r.save()

    return redirect("posts:detail", post_id=post.id)

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not can_moderate(request.user, post.community):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()

    if request.method == "POST":
        post.is_deleted = True
        post.save()
        return redirect("posts:home_feed")

    return redirect("posts:detail", post_id=post.id)

@login_required
def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author and not can_moderate(request.user, post.community):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()

    if request.method == "POST":
        comment.is_deleted = True
        comment.save()

    return redirect("posts:detail", post_id=post.id)

def search(request):
    q = request.GET.get("q", "").strip()
    post_results = []
    community_results = []

    if q:
        post_results = Post.objects.filter(
            is_deleted=False
        ).filter(
            Q(title__icontains=q) | Q(body__icontains=q)
        ).select_related("community", "author")[:20]

        community_results = Community.objects.filter(
            Q(name__icontains=q) | Q(title__icontains=q)
        )[:10]

    return render(request, "search/results.html", {
        "q": q,
        "post_results": post_results,
        "community_results": community_results,
    })