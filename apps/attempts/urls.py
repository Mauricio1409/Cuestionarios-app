from django.urls import path
from apps.attempts.views_web import start_attempt, take_attempt, submit_attempt, history_view, attempt_detail

app_name = "attempts"

urlpatterns = [
    path("start/<int:quiz_id>/", start_attempt, name="start"),
    path("take/<int:attempt_id>/", take_attempt, name="take"),
    path("submit/<int:attempt_id>/", submit_attempt, name="submit"),
    path("history/", history_view, name="history"),
    path("<int:attempt_id>/", attempt_detail, name="detail"),
]
