from django.urls import path
from . import views

app_name = "dm"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("<int:conversation_id>/", views.conversation_detail, name="detail"),
    path("<int:conversation_id>/delete/", views.delete_conversation, name="delete"),
    path("new/<str:username>/", views.new_conversation, name="new"),
    path("search/", views.user_search, name="user_search"),
    path("message/<int:message_id>/delete/", views.delete_message, name="delete_message"),
]