from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("accounts/", include("apps.users.urls")),
    path("", include("apps.subjects.urls")),
    path("", include("apps.quizzes.urls")),
    path("attempts/", include("apps.attempts.urls")),
    path("staff/", include("apps.quizzes.admin_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
