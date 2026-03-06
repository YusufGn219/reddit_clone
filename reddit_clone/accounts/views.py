from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm
from .models import User
from posts.models import Post, Comment
from .models import Notification

from .forms import ProfileAvatarForm
from .models import Profile

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kayıt başarıyla tamamlandı.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def profile_view(request, username: str):
    user_obj = get_object_or_404(User, username=username)
    tab = request.GET.get("tab", "posts")  # default: posts sekmesi

    if tab == "comments":
        items = Comment.objects.filter(
            author=user_obj,
            is_deleted=False
        ).select_related("post").order_by("-created_at")
    else:
        tab = "posts"
        items = Post.objects.filter(
            author=user_obj,
            is_deleted=False
        ).select_related("community").order_by("-created_at")

    return render(request, "accounts/profile.html", {
        "profile_user": user_obj,
        "items": items,
        "tab": tab,
    })

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        user = request.user
    ).select_related("comment__post", "comment__author")

    notifications.filter(is_read=False).update(is_read=True) # bildirimleri okundu olarak güncelle.

    return render(request, "accounts/notifications.html", {
        "notifications": notifications,
    })

@login_required
def avatar_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil resmi güncellendi.")
            return redirect("accounts:profile", username=request.user.username)
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, "accounts/avatar_edit.html", {
        "form": form,
    })