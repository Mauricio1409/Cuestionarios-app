from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.quizzes.models import Quiz, Question, QuestionOption


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempt_answers")
    is_correct = models.BooleanField(default=False)
    score_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)


class AttemptAnswerOption(models.Model):
    attempt_answer = models.ForeignKey(AttemptAnswer, on_delete=models.CASCADE, related_name="selected_options")
    question_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, related_name="selected_in")
    created_at = models.DateTimeField(auto_now_add=True)
