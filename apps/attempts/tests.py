from decimal import Decimal

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.attempts.models import QuizAttempt
from apps.quizzes.models import Question, QuestionOption, QuestionType, Quiz
from apps.subjects.models import Subject
from apps.users.models import User


class AttemptFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.other_user = User.objects.create_user(email="other@test.com", password="Pass1234!", name="Other")
        self.subject = Subject.objects.create(name="Historia", description="")

    def _build_quiz_with_questions(self, *, is_active=True):
        quiz = Quiz.objects.create(subject=self.subject, name="Quiz 1", is_active=is_active)
        q1 = Question.objects.create(
            quiz=quiz,
            statement="Capital de Francia",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=1,
        )
        q1_ok = QuestionOption.objects.create(question=q1, text="París", is_correct=True, position=1)
        QuestionOption.objects.create(question=q1, text="Lyon", is_correct=False, position=2)

        q2 = Question.objects.create(
            quiz=quiz,
            statement="Números pares",
            question_type=QuestionType.MULTIPLE_CHOICE,
            score=Decimal("2.00"),
            position=2,
        )
        q2_ok1 = QuestionOption.objects.create(question=q2, text="2", is_correct=True, position=1)
        q2_ok2 = QuestionOption.objects.create(question=q2, text="4", is_correct=True, position=2)
        QuestionOption.objects.create(question=q2, text="3", is_correct=False, position=3)
        return quiz, q1, q1_ok, q2, q2_ok1, q2_ok2

    def test_start_attempt_blocks_inactive_quiz(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Quiz inactivo", is_active=False)

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:start", args=[quiz.id]), follow=True)

        self.assertRedirects(response, reverse("quizzes:quizzes"))
        self.assertEqual(QuizAttempt.objects.count(), 0)

    def test_start_attempt_blocks_quiz_without_questions(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Quiz vacío", is_active=True)

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:start", args=[quiz.id]), follow=True)

        self.assertRedirects(response, reverse("quizzes:quizzes"))
        self.assertEqual(QuizAttempt.objects.count(), 0)

    def test_submit_attempt_scores_single_and_multiple_choice_exactly(self):
        quiz, q1, q1_ok, q2, q2_ok1, q2_ok2 = self._build_quiz_with_questions(is_active=True)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("attempts:submit", args=[attempt.id]),
            {
                f"question_{q1.id}": [str(q1_ok.id)],
                f"question_{q2.id}": [str(q2_ok1.id), str(q2_ok2.id)],
            },
        )

        self.assertEqual(response.status_code, 302)
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, Decimal("3.00"))
        self.assertEqual(attempt.total_score, Decimal("3.00"))
        self.assertIsNotNone(attempt.finished_at)
        self.assertEqual(attempt.answers.count(), 2)

    def test_history_is_isolated_by_user(self):
        quiz, *_ = self._build_quiz_with_questions(is_active=True)
        own_attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)
        QuizAttempt.objects.create(user=self.other_user, quiz=quiz)

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:history"))
        attempts = list(response.context["attempts"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(attempts, [own_attempt])

    def test_history_exposes_review_and_retry_actions(self):
        quiz, *_ = self._build_quiz_with_questions(is_active=True)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz, score=Decimal("1.00"), total_score=Decimal("3.00"))

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:history"))

        self.assertContains(response, reverse("attempts:detail", args=[attempt.id]))
        self.assertContains(response, reverse("attempts:start", args=[quiz.id]))
        self.assertContains(response, "Revisar intento")
        self.assertContains(response, "Volver a intentarlo")

    def test_take_attempt_renders_questions_ordered_by_position(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Orden", is_active=True)
        q2 = Question.objects.create(
            quiz=quiz,
            statement="Segunda",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=2,
        )
        q1 = Question.objects.create(
            quiz=quiz,
            statement="Primera",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=1,
        )
        QuestionOption.objects.create(question=q1, text="A", is_correct=True, position=1)
        QuestionOption.objects.create(question=q2, text="B", is_correct=True, position=1)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:take", args=[attempt.id]))

        ordered_questions = list(response.context["questions"])
        self.assertEqual([q.id for q in ordered_questions], [q1.id, q2.id])

    def test_attempt_detail_foreign_user_redirects_with_explicit_message(self):
        quiz, *_ = self._build_quiz_with_questions(is_active=True)
        attempt = QuizAttempt.objects.create(user=self.other_user, quiz=quiz)

        self.client.force_login(self.user)
        response = self.client.get(reverse("attempts:detail", args=[attempt.id]), follow=True)

        self.assertRedirects(response, reverse("attempts:history"))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any("No tenés permiso" in message for message in messages))

    def test_attempt_detail_shows_correct_and_incorrect_per_question(self):
        quiz, q1, q1_ok, q2, q2_ok1, _ = self._build_quiz_with_questions(is_active=True)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        self.client.force_login(self.user)
        self.client.post(
            reverse("attempts:submit", args=[attempt.id]),
            {
                f"question_{q1.id}": [str(q1_ok.id)],
                f"question_{q2.id}": [str(q2_ok1.id)],
            },
        )
        response = self.client.get(reverse("attempts:detail", args=[attempt.id]))

        self.assertContains(response, "Correcta")
        self.assertContains(response, "Incorrecta")
        self.assertContains(response, "Capital de Francia")
        self.assertContains(response, "Números pares")
        self.assertContains(response, "Volver a intentarlo")
        self.assertContains(response, reverse("attempts:start", args=[quiz.id]))


class AttemptAdminFiltersTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True)
        self.user = User.objects.create_user(email="alice@test.com", password="Pass1234!", name="Alice")
        self.subject = Subject.objects.create(name="QA", description="")
        self.quiz_a = Quiz.objects.create(subject=self.subject, name="Álgebra", is_active=True)
        self.quiz_b = Quiz.objects.create(subject=self.subject, name="Historia", is_active=True)
        QuizAttempt.objects.create(user=self.user, quiz=self.quiz_a, score=1, total_score=2)
        QuizAttempt.objects.create(user=self.user, quiz=self.quiz_b, score=2, total_score=2)

    def test_admin_filters_by_quiz_name(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("admin-ui:attempt-list"), {"quiz": "Álgebra"})

        attempts = list(response.context["attempts"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0].quiz.name, "Álgebra")

    def test_admin_filters_by_user_email(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("admin-ui:attempt-list"), {"user": "alice"})

        attempts = list(response.context["attempts"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(attempts), 2)
