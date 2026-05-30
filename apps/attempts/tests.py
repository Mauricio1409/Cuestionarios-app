from decimal import Decimal

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.attempts.models import QuizAttempt
from apps.attempts.services.attempt_service import AttemptService
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

    def test_take_attempt_randomizes_questions_stably_per_attempt(self):
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
        q3 = Question.objects.create(
            quiz=quiz,
            statement="Tercera",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=3,
        )
        q4 = Question.objects.create(
            quiz=quiz,
            statement="Cuarta",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=4,
        )
        QuestionOption.objects.create(question=q1, text="A", is_correct=True, position=1)
        QuestionOption.objects.create(question=q2, text="B", is_correct=True, position=1)
        QuestionOption.objects.create(question=q3, text="C", is_correct=True, position=1)
        QuestionOption.objects.create(question=q4, text="D", is_correct=True, position=1)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        self.client.force_login(self.user)
        response_a = self.client.get(reverse("attempts:take", args=[attempt.id]))
        response_b = self.client.get(reverse("attempts:take", args=[attempt.id]))

        question_ids_a = [q.id for q in response_a.context["questions"]]
        question_ids_b = [q.id for q in response_b.context["questions"]]

        self.assertEqual(question_ids_a, question_ids_b)
        self.assertCountEqual(question_ids_a, [q1.id, q2.id, q3.id, q4.id])
        self.assertNotEqual(question_ids_a, [q1.id, q2.id, q3.id, q4.id])

    def test_take_attempt_randomizes_options_stably_per_attempt(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Opciones", is_active=True)
        question = Question.objects.create(
            quiz=quiz,
            statement="Elegí una",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=1,
        )
        option_a = QuestionOption.objects.create(question=question, text="A", is_correct=False, position=1)
        option_b = QuestionOption.objects.create(question=question, text="B", is_correct=True, position=2)
        option_c = QuestionOption.objects.create(question=question, text="C", is_correct=False, position=3)
        option_d = QuestionOption.objects.create(question=question, text="D", is_correct=False, position=4)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        ordered_question = AttemptService().questions_for_attempt_display(attempt)[0]
        shuffled_ids_first = [option.id for option in ordered_question.shuffled_options]
        shuffled_ids_second = [option.id for option in AttemptService().questions_for_attempt_display(attempt)[0].shuffled_options]

        self.assertEqual(shuffled_ids_first, shuffled_ids_second)
        self.assertCountEqual(shuffled_ids_first, [option_a.id, option_b.id, option_c.id, option_d.id])
        self.assertNotEqual(shuffled_ids_first, [option_a.id, option_b.id, option_c.id, option_d.id])

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

    def test_attempt_detail_reuses_same_question_and_option_order_as_attempt(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Orden revisión", is_active=True)
        q1 = Question.objects.create(
            quiz=quiz,
            statement="Primera",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=1,
        )
        q2 = Question.objects.create(
            quiz=quiz,
            statement="Segunda",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=2,
        )
        q3 = Question.objects.create(
            quiz=quiz,
            statement="Tercera",
            question_type=QuestionType.SINGLE_CHOICE,
            score=Decimal("1.00"),
            position=3,
        )
        q1a = QuestionOption.objects.create(question=q1, text="A1", is_correct=True, position=1)
        q1b = QuestionOption.objects.create(question=q1, text="B1", is_correct=False, position=2)
        QuestionOption.objects.create(question=q2, text="A2", is_correct=True, position=1)
        QuestionOption.objects.create(question=q2, text="B2", is_correct=False, position=2)
        QuestionOption.objects.create(question=q3, text="A3", is_correct=True, position=1)
        QuestionOption.objects.create(question=q3, text="B3", is_correct=False, position=2)
        attempt = QuizAttempt.objects.create(user=self.user, quiz=quiz)

        self.client.force_login(self.user)
        take_response = self.client.get(reverse("attempts:take", args=[attempt.id]))
        take_question_ids = [question.id for question in take_response.context["questions"]]
        take_first_question_option_ids = [option.id for option in take_response.context["questions"][0].shuffled_options]

        self.client.post(
            reverse("attempts:submit", args=[attempt.id]),
            {
                f"question_{q1.id}": [str(q1a.id)],
                f"question_{q2.id}": [],
                f"question_{q3.id}": [],
            },
        )
        detail_response = self.client.get(reverse("attempts:detail", args=[attempt.id]))
        ordered_answers = detail_response.context["ordered_answers"]

        self.assertEqual([answer.question_id for answer in ordered_answers], take_question_ids)
        self.assertEqual([option["id"] for option in ordered_answers[0].review_options], take_first_question_option_ids)


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
