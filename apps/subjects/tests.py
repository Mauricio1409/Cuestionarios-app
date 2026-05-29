from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from apps.subjects.models import Subject
from apps.subjects.services.subject_service import SubjectService
from apps.users.models import User


class SubjectCatalogTests(TestCase):
    def test_subject_catalog_lists_subjects_for_authenticated_user(self):
        user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        subject = Subject.objects.create(name="Programación", description="")

        self.client.force_login(user)
        response = self.client.get(reverse("catalog:subjects"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(subject, list(response.context["subjects"]))


class SubjectServiceTests(TestCase):
    def test_create_subject_valid(self):
        subject = SubjectService().create_subject({"name": "Redes", "description": ""})

        self.assertEqual(subject.name, "Redes")

    def test_create_subject_invalid_empty_name(self):
        with self.assertRaises(ValidationError):
            SubjectService().create_subject({"name": "   ", "description": ""})
