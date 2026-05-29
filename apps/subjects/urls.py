from django.urls import path

from apps.subjects.views_web import subject_catalog, subject_create, subject_delete, subject_edit

app_name = "catalog"

urlpatterns = [
    path("subjects/", subject_catalog, name="subjects"),
    path("subjects/new/", subject_create, name="subject-create"),
    path("subjects/<int:subject_id>/edit/", subject_edit, name="subject-edit"),
    path("subjects/<int:subject_id>/delete/", subject_delete, name="subject-delete"),
]
