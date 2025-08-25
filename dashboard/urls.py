from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
   #S path("", views.dashboard, name="dashboard"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("add-project/", views.add_project, name="add_project"),
    path("send-message/<int:user_id>/", views.send_message, name="send_message"),
    path("mark-read/<int:notif_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("dashboard/", views.dashboard, name="dashboard"),
     path("", views.dashboard, name="dashboard"),
    # connections
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    # feed
    path("feed/", views.feed, name="feed"),
    # search
    path("search/", views.search, name="search"),
    # endorsements
    path("endorse/<int:skill_id>/", views.endorse_skill, name="endorse_skill"),
    # settings
    path("settings/", views.settings_page, name="settings_page"),
]
