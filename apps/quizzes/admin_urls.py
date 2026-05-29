from django.urls import path

from apps.quizzes.views_web import (
    AdminDashboardView,
    admin_option_create,
    admin_question_create,
    admin_question_delete,
    admin_question_edit,
    admin_question_list,
    admin_quiz_create,
    admin_quiz_delete,
    admin_quiz_edit,
    admin_quiz_list,
)
from apps.attempts.views_web import admin_attempt_list

app_name = "admin-ui"

urlpatterns = [
    path("", AdminDashboardView.as_view(), name="dashboard"),
    path("quizzes/", admin_quiz_list, name="quiz-list"),
    path("quizzes/new/", admin_quiz_create, name="quiz-create"),
    path("quizzes/<int:quiz_id>/edit/", admin_quiz_edit, name="quiz-edit"),
    path("quizzes/<int:quiz_id>/delete/", admin_quiz_delete, name="quiz-delete"),
    path("quizzes/<int:quiz_id>/questions/", admin_question_list, name="question-list"),
    path("quizzes/<int:quiz_id>/questions/new/", admin_question_create, name="question-create"),
    path("questions/<int:question_id>/edit/", admin_question_edit, name="question-edit"),
    path("questions/<int:question_id>/delete/", admin_question_delete, name="question-delete"),
    path("questions/<int:question_id>/options/new/", admin_option_create, name="option-create"),
    path("attempts/", admin_attempt_list, name="attempt-list"),
]
