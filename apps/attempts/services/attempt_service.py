import random

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

    def _shuffle_questions_and_options(self, attempt, questions):
        questions = list(questions)

        question_random = random.Random(f"attempt:{attempt.id}:questions")
        question_random.shuffle(questions)

        for question in questions:
            options = list(question.options.all())
            option_random = random.Random(f"attempt:{attempt.id}:question:{question.id}:options")
            option_random.shuffle(options)
            question.shuffled_options = options

        return questions

    def questions_for_attempt_display(self, attempt):
        questions = self.repo.questions_for_quiz(attempt.quiz)
        return self._shuffle_questions_and_options(attempt, questions)

    def ordered_review_answers(self, attempt):
        question_order = self._shuffle_questions_and_options(attempt, self.repo.questions_for_quiz(attempt.quiz))
        answers_by_question_id = {answer.question_id: answer for answer in attempt.answers.all()}
        ordered_answers = []

        for question in question_order:
            answer = answers_by_question_id.get(question.id)
            if not answer:
                continue

            selected_option_ids = {selected.question_option_id for selected in answer.selected_options.all()}
            answer.review_options = [
                {
                    "id": option.id,
                    "text": option.text,
                    "is_correct": option.is_correct,
                    "is_selected": option.id in selected_option_ids,
                }
                for option in question.shuffled_options
            ]
            ordered_answers.append(answer)

        return ordered_answers

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
