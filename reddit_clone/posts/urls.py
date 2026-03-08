from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("feed/", views.home_feed, name="home_feed"),
    path("create/", views.post_create, name="post_create"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    path("<int:post_id>/comment/", views.comment_create, name="comment_create"),
    path("<int:post_id>/reply/<int:parent_id>/", views.reply_create, name="reply_create"),
    path("<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("<int:post_id>/comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
    path("<int:post_id>/save/", views.save_post, name="save_post"),
]
