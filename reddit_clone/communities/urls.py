from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("create/", views.community_create, name="create"),
    path("<str:name>/", views.community_detail, name="detail"),
    path("<str:name>/edit/", views.community_edit, name="edit"),
    path("<str:name>/mod/add", views.add_moderator, name="add_moderator"),
]