from django.urls import path
from apps.users.views.logout_views import LogOutView
from apps.users.views.web_views import signup_view, login_view, logout_view, profile_view

app_name = "accounts"

urlpatterns = [
    path("api/logout/", LogOutView.as_view(), name="api-logout"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
]
