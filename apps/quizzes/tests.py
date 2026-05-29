from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.quizzes.models import Quiz, Question, QuestionType
from apps.quizzes.services.quiz_service import QuestionDomainService
from apps.subjects.models import Subject
from apps.users.models import User


class QuizCatalogAndAdminAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        self.subject = Subject.objects.create(name="Matemática", description="")

    def test_catalog_only_lists_active_quizzes(self):
        active = Quiz.objects.create(subject=self.subject, name="Activo", is_active=True)
        Quiz.objects.create(subject=self.subject, name="Inactivo", is_active=False)

        self.client.force_login(self.user)
        response = self.client.get(reverse("quizzes:quizzes"))

        self.assertEqual(response.status_code, 200)
        quizzes = list(response.context["quizzes"])
        self.assertEqual(quizzes, [active])

    def test_admin_ui_redirects_non_staff(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin-ui:quiz-list"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:subjects"))

    def test_admin_ui_allows_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("admin-ui:quiz-list"))
        self.assertEqual(response.status_code, 200)

    def test_quiz_creation_keeps_subject_association(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("admin-ui:quiz-create"),
            {
                "subject": self.subject.id,
                "name": "Parcial 1",
                "description": "desc",
                "is_active": True,
            },
        )

        self.assertRedirects(response, reverse("admin-ui:quiz-list"))
        quiz = Quiz.objects.get(name="Parcial 1")
        self.assertEqual(quiz.subject_id, self.subject.id)

    def test_non_image_upload_is_rejected(self):
        quiz = Quiz.objects.create(subject=self.subject, name="Con imágenes", is_active=True)
        fake_txt = SimpleUploadedFile("nota.txt", b"no es imagen", content_type="text/plain")

        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("admin-ui:question-create", args=[quiz.id]),
            {
                "statement": "",
                "image": fake_txt,
                "question_type": QuestionType.SINGLE_CHOICE,
                "score": "1.00",
                "explanation": "",
                "position": 1,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload a valid image")


class QuestionDomainValidationTests(TestCase):
    def test_question_allows_only_image(self):
        QuestionDomainService().validate_question_content("", object())

    def test_question_rejects_empty_statement_and_image(self):
        with self.assertRaises(ValidationError):
            QuestionDomainService().validate_question_content("", None)

    def test_single_choice_requires_exactly_one_correct_option(self):
        subject = Subject.objects.create(name="Sistemas")
        quiz = Quiz.objects.create(subject=subject, name="Quiz", is_active=True)
        question = Question.objects.create(
            quiz=quiz,
            statement="Q1",
            question_type=QuestionType.SINGLE_CHOICE,
            score="1.00",
            position=1,
        )

        with self.assertRaises(ValidationError):
            QuestionDomainService().validate_correct_options(question, [])

    def test_multiple_choice_requires_at_least_one_correct_option(self):
        subject = Subject.objects.create(name="Sistemas")
        quiz = Quiz.objects.create(subject=subject, name="Quiz", is_active=True)
        question = Question.objects.create(
            quiz=quiz,
            statement="Q2",
            question_type=QuestionType.MULTIPLE_CHOICE,
            score="1.00",
            position=1,
        )

        with self.assertRaises(ValidationError):
            QuestionDomainService().validate_correct_options(question, [])
