from django.contrib import admin
from apps.attempts.models import QuizAttempt, AttemptAnswer, AttemptAnswerOption

admin.site.register(QuizAttempt)
admin.site.register(AttemptAnswer)
admin.site.register(AttemptAnswerOption)
