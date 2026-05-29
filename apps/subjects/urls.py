from django.urls import path
from apps.subjects.views_web import subject_catalog

app_name = "catalog"

urlpatterns = [
    path("subjects/", subject_catalog, name="subjects"),
]
