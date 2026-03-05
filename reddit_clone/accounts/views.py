from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render

from .forms import RegisterForm
from .models import User

def register_view (request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form":form})

def profile_view(request, username: str):
    user_obj = get_object_or_404(User, username=username)
    return render(request, "accounts/profile.html", {"profile_user": user_obj})