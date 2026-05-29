from django.urls import path

from apps.users.views.logout_views import LogOutView

urlpatterns = [
    path('logout/', LogOutView.as_view(), name='logout'),
]

