from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("avatar/edit/", views.avatar_edit, name="avatar_edit"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("verify/<uuid:token>/", views.verify_email, name = "verify_email"),
    path("u/<str:username>/follow/", views.follow_user, name="follow_user"),
    
]