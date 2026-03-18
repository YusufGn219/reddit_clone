from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("create/", views.community_create, name="create"),
    path("<str:name>/", views.community_detail, name="detail"),
    path("<str:name>/edit/", views.community_edit, name="edit"),
    path("<str:name>/mod/add", views.add_moderator, name="add_moderator"),
    path("<str:name>/rules/add/", views.rule_add, name = "rule_add"),
    path("<str:name>/rules/<int:rule_id>/delete/", views.rule_delete, name="rule_delete"),
    path("<str:name>/mod/remove/<int:user_id>/", views.remove_moderator, name="remove_moderator"),
    path("<str:name>/ban/<int:user_id>/", views.ban_user, name="ban_user"),
    path("<str:name>/unban/<int:user_id>/", views.unban_user, name="unban_user"),
    path("<str:name>/join/", views.join_community, name="join"),
]