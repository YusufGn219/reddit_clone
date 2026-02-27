from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Comment
from .forms import PostCreateForm, CommentForm
from .services.comments import build_comment_tree
from django.db.models import Sum
from .services.querysets import with_post_score
from votes.models import CommentVote


def home(request):
    qs = Post.objects.select_related("community", "author")
    qs = with_post_score(qs).order_by("-created_at")  # new default

    paginator = Paginator(qs, 10)  # sayfa başı 10 post
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj, "posts": page_obj.object_list})


def home_feed(request):
    posts = Post.objects.filter(is_deleted=False).order_by("-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/home_feed.html", {"page_obj": page_obj})


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
