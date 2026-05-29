from django.urls import path, include

urlpatterns = [
    # Autenticación
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/auth/", include("apps.users.urls")),
]
