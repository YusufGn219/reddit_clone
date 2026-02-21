from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostCreateForm
from communities.models import Community

def home(request):
    return HttpResponse("Home")

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", post_id =post.id)
    else:
        form = PostCreateForm()
    return render(request, "posts/post_create.html", {"form": form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id = post_id, is_deleted = False)
    return render(request, "posts/post_detail.html", {"post": post})

def home_feed(request):
    posts = Post.objects.filter(is_deleted=False).order_by("-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/home_feed.html", {"page_obj": page_obj})