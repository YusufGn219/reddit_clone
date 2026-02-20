from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path("create/", views.community_create, name="create"),
    path("<str:name>/", views.community_detail, name="detail"),
]