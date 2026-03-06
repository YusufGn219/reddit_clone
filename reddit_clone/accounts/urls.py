from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("notifications/", views.notifications_view, name="notifications")
]