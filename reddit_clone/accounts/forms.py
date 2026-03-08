from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "display_name"]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio", "avatar"]