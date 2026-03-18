from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib import messages

from .forms import CommunityCreateForm, CommunityEditForm
from .models import Community, CommunityModerator, CommunityRule, BannedUser, CommunityMember
from .permissions import can_moderate, is_community_owner

from posts.models import Post
from posts.services.sorting import normalize_sort_and_time, apply_sort



@login_required
def community_create(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()

            CommunityModerator.objects.create(
                community=community,
                user=request.user
            )

            messages.success(request, "Topluluk başarıyla oluşturuldu.")
            return redirect("communities:detail", name=community.name)
    else:
        form = CommunityCreateForm()

    return render(request, "communities/community_create.html", {
        "form": form,
    })


def community_detail(request, name):
    community = get_object_or_404(Community, name=name)

    sort, t = normalize_sort_and_time(request.GET)

    qs = Post.objects.filter(
        community=community,
        is_deleted=False
    ).select_related("author")

    qs = apply_sort(qs, sort, t)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    member_count = community.members.count()
    is_member = False
    if request.user.is_authenticated:
        is_member = CommunityMember.objects.filter(
            community=community,
            user=request.user
        ).exists()

    return render(request, "communities/community_detail.html", {
        "community": community,
        "page_obj": page_obj,
        "sort": sort,
        "t": t,
        "member_count": member_count,
        "is_member": is_member,
    })


@login_required
def community_edit(request, name):
    community = get_object_or_404(Community, name=name)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        form = CommunityEditForm(request.POST, request.FILES, instance=community)
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

    User = get_user_model()
    query = ""

    existing_mod_ids = community.moderators.values_list("user_id", flat=True)

    base_users = User.objects.exclude(
        id__in=existing_mod_ids
    ).exclude(
        id=community.created_by.id
    ).order_by("username")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "search":
            query = request.POST.get("username", "").strip()

            if query:
                search_results = base_users.filter(username__icontains=query)[:10]
            else:
                search_results = base_users[:10]

        elif action == "add":
            username = request.POST.get("username", "").strip()

            try:
                user = User.objects.get(username=username)

                _, created = CommunityModerator.objects.get_or_create(
                    community=community,
                    user=user
                )

                if created:
                    messages.success(request, f"{username} moderatör olarak eklendi.")
                else:
                    messages.error(request, f"{username} zaten moderatör.")

            except User.DoesNotExist:
                messages.error(request, "Kullanıcı bulunamadı.")

            return redirect("communities:add_moderator", name=community.name)

        else:
            search_results = base_users[:10]

    else:
        search_results = base_users[:10]

    current_mods = CommunityModerator.objects.filter(
        community=community
    ).select_related("user").exclude(
        user=community.created_by
    )

    return render(request, "communities/add_moderator.html", {
        "community": community,
        "search_results": search_results,
        "current_mods": current_mods,
        "query": query,
    })

@login_required
def remove_moderator(request, name, user_id):
    community = get_object_or_404(Community, name=name)

    if not is_community_owner(request.user, community):
        return HttpResponseForbidden()

    moderator = get_object_or_404(
        CommunityModerator,
        community=community,
        user_id=user_id
    )

    # Owner kendisini moderatör listesinden silemesin
    if moderator.user == community.created_by:
        messages.error(request, "Topluluk sahibi moderatörlükten çıkarılamaz.")
        return redirect("communities:add_moderator", name=community.name)

    if request.method == "POST":
        username = moderator.user.username
        moderator.delete()
        messages.success(request, f"{username} moderatörlükten çıkarıldı.")

    return redirect("communities:add_moderator", name=community.name)

@login_required
def rule_add(request, name):
    community = get_object_or_404(Community, name=name)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            order = community.rules.count() + 1

            CommunityRule.objects.create(
                community=community,
                title=title,
                description=description,
                order=order
            )

            messages.success(request, "Kural başarıyla eklendi.")

        return redirect("communities:detail", name=community.name)

    return render(request, "communities/rule_add.html", {
        "community": community,
    })


@login_required
def rule_delete(request, name, rule_id):
    community = get_object_or_404(Community, name=name)
    rule = get_object_or_404(CommunityRule, pk=rule_id, community=community)

    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        rule.delete()
        messages.success(request, "Kural başarıyla silindi.")

    return redirect("communities:detail", name=community.name)

@login_required
def ban_user(request, name, user_id):
    community = get_object_or_404(Community, name=name)
    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    if user == community.created_by:
        messages.error(request, "Topluluk sahibi banlanamaz.")
        return redirect("communities:detail", name=community.name)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        _, created = BannedUser.objects.get_or_create(
            community=community,
            user=user,
            defaults={"banned_by": request.user, "reason": reason}
        )
        if created:
            messages.success(request, f"{user.username} banlandı.")
        else:
            messages.error(request, f"{user.username} zaten banlı.")

    return redirect("communities:detail", name=community.name)


@login_required
def unban_user(request, name, user_id):
    community = get_object_or_404(Community, name=name)
    if not can_moderate(request.user, community):
        return HttpResponseForbidden()

    if request.method == "POST":
        BannedUser.objects.filter(community=community, user_id=user_id).delete()
        messages.success(request, "Ban kaldırıldı.")

    return redirect("communities:detail", name=community.name)

@login_required
def join_community (request,name):
    community=get_object_or_404(Community,name=name)

    if request.method == "POST":
        member , created = CommunityMember.objects.get_or_create(
            community=community,
            user=request.user
        )
        if not created:
            member.delete()
    
    return redirect ("communties:detail", name=community.name)