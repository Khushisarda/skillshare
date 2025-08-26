from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("", views.club_list, name="club_list"),                                    # /clubs/
    path("<slug:slug>/", views.club_detail, name="club_detail"),                    # /clubs/<club_name>/
    path("<slug:slug>/posts/add/", views.add_post, name="add_post"),                # add post
    path("<slug:slug>/posts/<int:pk>/edit/", views.edit_post, name="edit_post"),    # edit post
    path("<slug:slug>/posts/<int:pk>/delete/", views.delete_post, name="delete_post"),
]
