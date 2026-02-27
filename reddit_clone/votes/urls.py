from django.urls import path
from . import views

app_name = "votes"

urlpatterns = [
    path("post/<int:post_id>/", views.vote_post, name="post"),
    path("comment/<int:comment_id>/", views.vote_comment, name="comment"),
]