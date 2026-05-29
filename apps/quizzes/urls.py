from django.urls import path
from apps.quizzes.views_web import quiz_catalog

app_name = "quizzes"

urlpatterns = [
    path("quizzes/", quiz_catalog, name="quizzes"),
]
