from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import CommunityCreateForm
from .models import Community
from posts.models import Post

@login_required
def community_create(request):
    if request.method == "POST":
        form= CommunityCreateForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            return redirect("communities:detail", name=community.name)

    else:
        form = CommunityCreateForm()
    return render(request, "communities/community_create.html", {"form": form})

def community_detail(request, name):
    community = get_object_or_404(Community, name=name)

    posts = Post.objects.filter(
        community=community,
        is_deleted=False
    ).order_by("-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "communities/community_detail.html", {
        "community": community,
        "page_obj": page_obj
    })