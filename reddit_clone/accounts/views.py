from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm
from .models import User
from posts.models import Post, Comment, SavedPost
from .models import Notification

from .forms import ProfileAvatarForm, ProfileEditForm, RegisterForm
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import EmailVerification

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = EmailVerification.objects.create(user=user)
            verify_url = request.build_absolute_uri(
                f"/verify/{token.token}/"
            )
            send_mail(
                subject="E-posta Doğrulama HK",
                message=f"Merhaba {user.username}, \n\n Hesabınızı doğrulama linki: \n {verify_url}",
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            login(request, user)
            messages.info(request, "Kayıt başarıyla tamamlandı. E-posta adresinize doğrulama linki gönderildi.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def verify_email(request, token):
    try:
        t=EmailVerification.objects.get(token=token)
        t.user.is_email_verified =True
        t.user.save()
        t.delete()
        messages.success(request,"E-posta adresininz başarıyla doğrulandı.")
        
    except EmailVerification.DoesNotExist:
        messages.error(request, "Doğrulama linki geçersiz veya süresi dolmuş.")
    
    return redirect("home")

def profile_view(request, username: str):
    user_obj = get_object_or_404(User, username=username)
    tab = request.GET.get("tab", "posts")

    if tab == "comments":
        items = Comment.objects.filter(
            author=user_obj,
            is_deleted=False
        ).select_related("post").order_by("-created_at")

    elif tab == "saved":
        if request.user.is_authenticated and request.user == user_obj:
            items = SavedPost.objects.filter(
                user=user_obj,
                post__is_deleted=False  # silinmiş postları gösterme
            ).select_related("post__community").order_by("-saved_at")
        else:
            items = SavedPost.objects.none()

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
        user=request.user
    ).select_related("comment__post", "comment__author")

    notifications.filter(is_read=False).update(is_read=True)

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

@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user = request.user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil güncellendi.")
            return redirect("accounts:profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {
        "form": form,
    })