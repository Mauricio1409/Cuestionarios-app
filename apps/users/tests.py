from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class WebAuthAccessTests(TestCase):
    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_signup_requires_authentication(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_non_staff_cannot_access_signup(self):
        user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:subjects"))

    def test_staff_can_access_signup(self):
        staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        self.client.force_login(staff)

        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_profile(self):
        user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)


class WebAuthFlowTests(TestCase):
    def test_staff_signup_success_hashes_password_without_switching_session(self):
        staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        self.client.force_login(staff)

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "nuevo@test.com",
                "name": "Nuevo",
                "password1": "Pass1234!",
                "password2": "Pass1234!",
            },
        )

        self.assertRedirects(response, reverse("accounts:signup"))
        user = User.objects.get(email="nuevo@test.com")
        self.assertNotEqual(user.password, "Pass1234!")
        self.assertTrue(user.password.startswith("pbkdf2_"))
        self.assertTrue(user.check_password("Pass1234!"))
        self.assertEqual(self.client.session.get("_auth_user_id"), str(staff.id))

    def test_login_invalid_shows_actionable_feedback(self):
        User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")

        response = self.client.post(
            reverse("accounts:login"),
            {"email": "user@test.com", "password": "Incorrecta123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciales inválidas")
        self.assertContains(response, "value=\"user@test.com\"", html=False)


class UserRegistrationApiAccessTests(APITestCase):
    def test_registration_api_rejects_anonymous(self):
        response = self.client.post(
            "/api/auth/users/",
            {
                "email": "anon@test.com",
                "name": "Anon",
                "password": "Pass1234!",
                "re_password": "Pass1234!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_api_rejects_authenticated_non_staff(self):
        user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/auth/users/",
            {
                "email": "otro@test.com",
                "name": "Otro",
                "password": "Pass1234!",
                "re_password": "Pass1234!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registration_api_allows_staff(self):
        staff = User.objects.create_user(
            email="staff@test.com", password="Pass1234!", name="Staff", is_staff=True
        )
        self.client.force_authenticate(user=staff)

        response = self.client.post(
            "/api/auth/users/",
            {
                "email": "nuevo-api@test.com",
                "name": "Nuevo API",
                "password": "Pass1234!",
                "re_password": "Pass1234!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="nuevo-api@test.com").exists())
