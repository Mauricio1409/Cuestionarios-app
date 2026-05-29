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

    def test_staff_catalog_shows_management_actions(self):
        staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        subject = Subject.objects.create(name="Redes", description="")

        self.client.force_login(staff)
        response = self.client.get(reverse("catalog:subjects"))

        self.assertContains(response, reverse("catalog:subject-create"))
        self.assertContains(response, reverse("catalog:subject-edit", args=[subject.id]))
        self.assertContains(response, reverse("catalog:subject-delete", args=[subject.id]))


class SubjectManagementViewsTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        self.user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.subject = Subject.objects.create(name="Programación", description="Base")

    def test_non_staff_cannot_access_subject_create(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("catalog:subject-create"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:subjects"))

    def test_staff_can_create_subject(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("catalog:subject-create"),
            {"name": "Bases", "description": "Datos persistentes"},
            follow=True,
        )

        self.assertRedirects(response, reverse("catalog:subjects"))
        self.assertTrue(Subject.objects.filter(name="Bases").exists())

    def test_staff_can_edit_subject(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("catalog:subject-edit", args=[self.subject.id]),
            {"name": "Programación Avanzada", "description": "POO"},
            follow=True,
        )

        self.assertRedirects(response, reverse("catalog:subjects"))
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, "Programación Avanzada")

    def test_staff_can_delete_subject(self):
        self.client.force_login(self.staff)

        response = self.client.post(reverse("catalog:subject-delete", args=[self.subject.id]), follow=True)

        self.assertRedirects(response, reverse("catalog:subjects"))
        self.assertFalse(Subject.objects.filter(id=self.subject.id).exists())


class SubjectServiceTests(TestCase):
    def test_create_subject_valid(self):
        subject = SubjectService().create_subject({"name": "Redes", "description": ""})

        self.assertEqual(subject.name, "Redes")

    def test_create_subject_invalid_empty_name(self):
        with self.assertRaises(ValidationError):
            SubjectService().create_subject({"name": "   ", "description": ""})
