from django.db.models import Count

from apps.quizzes.models import Quiz, Question


class QuizRepository:
    def list_all(self):
        return Quiz.objects.select_related("subject").annotate(question_count=Count("questions", distinct=True))

    def list_active(self):
        return Quiz.objects.select_related("subject").filter(is_active=True).annotate(
            question_count=Count("questions", distinct=True)
        )

    def get(self, pk: int):
        return Quiz.objects.select_related("subject").filter(pk=pk).first()

    def create(self, **data):
        return Quiz.objects.create(**data)

    def update(self, quiz: Quiz, **data):
        for k, v in data.items():
            setattr(quiz, k, v)
        quiz.save()
        return quiz

    def delete(self, quiz: Quiz):
        quiz.delete()

    def has_questions(self, quiz: Quiz) -> bool:
        return Question.objects.filter(quiz=quiz).exists()
