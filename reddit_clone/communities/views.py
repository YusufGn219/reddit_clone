from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from .forms import CommunityCreateForm, CommunityEditForm
from .models import Community, CommunityModerator
from .permissions import can_moderate, is_community_owner
from posts.models import Post
from posts.services.sorting import normalize_sort_and_time, apply_sort
from django.contrib import messages
from .models import Community, CommunityModerator,CommunityRule

@login_required
def community_create(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            CommunityModerator.objects.create(community=community, user=request.user)
            messages.success(request, "Topluluk başarıyla oluşturuldu.")
            return redirect("communities:detail", name=community.name)
    else:
        form = CommunityCreateForm()
    return render(request, "communities/community_create.html", {"form": form})


def community_detail(request, name):
    community = get_object_or_404(Community, name=name)

    sort, t = normalize_sort_and_time(request.GET)
    qs = Post.objects.filter(community=community, is_deleted=False).select_related("author")
    qs = apply_sort(qs, sort, t)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "communities/community_detail.html", {
        "community": community,
        "page_obj": page_obj,
        "sort": sort,
        "t": t,
    })


@login_required
def community_edit(request, name):
    community = get_object_or_404(Community, name=name)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        form = CommunityEditForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, "Topluluk başarıyla güncellendi.")
            return redirect("communities:detail", name=community.name)
    else:
        form = CommunityEditForm(instance=community)

    return render(request, "communities/community_edit.html", {
        "community": community,
        "form": form,
    })


@login_required
def add_moderator(request, name):
    community = get_object_or_404(Community, name=name)

    if not is_community_owner(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            CommunityModerator.objects.get_or_create(community=community, user=user)
            messages.success(request, "Moderatör başarıyla eklendi.")
        except User.DoesNotExist:
            messages.error(request, "Kullanıcı bulunamadı.")
        return redirect("communities:detail", name=community.name)

    return render(request, "communities/add_moderator.html", {"community": community})

@login_required
def rule_add(request, name):
    community = get_object_or_404(Community,name=name)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            order=community.rules.count() +1
            CommunityRule.objects.create(
                community=community,
                title=title,
                description=description,
                order=order
            )
            messages.success(request, "Kural başarıyla eklendi.")
        
        return redirect("communities:detail", name=community.name)

    return render(request, "communities/rule_add.html", {"community": community})

@login_required
def rule_delete(request, name, rule_id):
    community = get_object_or_404(Community,name=name)
    rule = get_object_or_404(CommunityRule, pk=rule_id,community=community)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        rule.delete()
        messages.success(request, "Kural başarıyla silindi.")
        
    return redirect("communities:detail", name=community.name)