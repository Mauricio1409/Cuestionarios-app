from decimal import Decimal
from django.db import models
from apps.subjects.models import Subject


class Quiz(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="quizzes")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "single_choice", "Opción única"
    MULTIPLE_CHOICE = "multiple_choice", "Opción múltiple"


def question_image_upload_to(instance, filename):
    return f"questions/{filename}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    statement = models.TextField(blank=True)
    image = models.ImageField(upload_to=question_image_upload_to, blank=True, null=True)
    question_type = models.CharField(max_length=30, choices=QuestionType.choices)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("1.00"))
    explanation = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "id"]
        indexes = [models.Index(fields=["quiz", "position"])]

    def __str__(self) -> str:
        return f"{self.quiz.name} - Q{self.position}"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "id"]
        indexes = [models.Index(fields=["question", "position"])]

    def __str__(self) -> str:
        return self.text[:50]
