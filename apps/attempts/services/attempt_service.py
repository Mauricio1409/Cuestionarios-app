from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils import timezone

from apps.attempts.repositories.attempt_repository import AttemptRepository
from apps.quizzes.services.quiz_service import QuizService


class AttemptService:
    def __init__(self):
        self.repo = AttemptRepository()
        self.quiz_service = QuizService()

    def start_attempt(self, user, quiz_id):
        quiz = self.quiz_service.get_quiz(quiz_id)
        if not quiz:
            raise Http404("Quiz no encontrado.")
        if not self.quiz_service.can_take(quiz):
            raise ValidationError("Este quiz no se puede resolver: está inactivo o no tiene preguntas.")
        return self.repo.create_attempt(user, quiz)

    def get_user_attempt_or_404(self, user_id, attempt_id):
        attempt = self.repo.history_for_user(user_id).filter(pk=attempt_id).select_related("quiz").first()
        if not attempt:
            raise Http404("Intento no encontrado.")
        return attempt

    def history_for_user(self, user_id):
        return self.repo.history_for_user(user_id)

    def detail_for_user(self, attempt_id, user_id):
        return self.repo.detail_for_user(attempt_id, user_id)

    def admin_list(self, user_q=None, quiz_q=None):
        return self.repo.admin_list(user_q=user_q, quiz_q=quiz_q)

    def submit_attempt(self, attempt, payload):
        questions = self.repo.questions_for_quiz(attempt.quiz)
        score = 0
        total = 0
        for question in questions:
            selected_ids = set(payload.get(str(question.id), []))
            options = list(question.options.all())
            correct_ids = {str(o.id) for o in options if o.is_correct}
            selected_options = [o for o in options if str(o.id) in selected_ids]
            is_correct = selected_ids == correct_ids
            total += float(question.score)
            gained = float(question.score) if is_correct else 0
            score += gained
            self.repo.save_answer(attempt, question, is_correct, gained, selected_options)
        return self.repo.finish_attempt(attempt, score, total, timezone.now())
