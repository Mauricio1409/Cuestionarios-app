from apps.attempts.models import QuizAttempt, AttemptAnswer, AttemptAnswerOption


class AttemptRepository:
    def create_attempt(self, user, quiz):
        return QuizAttempt.objects.create(user=user, quiz=quiz)

    def get_attempt(self, attempt_id):
        return QuizAttempt.objects.select_related("quiz", "user").filter(pk=attempt_id).first()

    def save_answer(self, attempt, question, is_correct, score_obtained, selected_options):
        ans = AttemptAnswer.objects.create(
            attempt=attempt,
            question=question,
            is_correct=is_correct,
            score_obtained=score_obtained,
        )
        for opt in selected_options:
            AttemptAnswerOption.objects.create(attempt_answer=ans, question_option=opt)
        return ans

    def history_for_user(self, user_id):
        return QuizAttempt.objects.filter(user_id=user_id).select_related("quiz", "quiz__subject").order_by("-started_at")

    def detail_for_user(self, attempt_id, user_id):
        return QuizAttempt.objects.filter(pk=attempt_id, user_id=user_id).prefetch_related(
            "answers__question", "answers__selected_options__question_option"
        ).first()

    def admin_list(self, user_q=None, quiz_q=None):
        qs = QuizAttempt.objects.select_related("user", "quiz", "quiz__subject").order_by("-started_at")
        if user_q:
            qs = qs.filter(user__email__icontains=user_q)
        if quiz_q:
            qs = qs.filter(quiz__name__icontains=quiz_q)
        return qs

    def questions_for_quiz(self, quiz):
        return quiz.questions.prefetch_related("options").order_by("position")

    def finish_attempt(self, attempt, score, total_score, finished_at):
        attempt.score = score
        attempt.total_score = total_score
        attempt.finished_at = finished_at
        attempt.save()
        return attempt
