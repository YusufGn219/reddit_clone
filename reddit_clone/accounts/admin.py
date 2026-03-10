from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Notification, EmailVerification

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Email Doğrulama", {"fields": ("is_email_verified",)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(EmailVerification)