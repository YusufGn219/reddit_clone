from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CommunityCreateForm
from .models import Community

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
    return render(request, "communities/community_detail.html", {"community": community})