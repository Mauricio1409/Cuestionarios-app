from django.test import TestCase
from django.urls import reverse

from apps.users.models import User


class WebAuthAccessTests(TestCase):
    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_authenticated_user_can_access_profile(self):
        user = User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)


class WebAuthFlowTests(TestCase):
    def test_signup_success_hashes_password(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "nuevo@test.com",
                "name": "Nuevo",
                "password1": "Pass1234!",
                "password2": "Pass1234!",
            },
        )

        self.assertRedirects(response, reverse("catalog:subjects"))
        user = User.objects.get(email="nuevo@test.com")
        self.assertNotEqual(user.password, "Pass1234!")
        self.assertTrue(user.password.startswith("pbkdf2_"))
        self.assertTrue(user.check_password("Pass1234!"))

    def test_login_invalid_shows_actionable_feedback(self):
        User.objects.create_user(email="user@test.com", password="Pass1234!", name="User")

        response = self.client.post(
            reverse("accounts:login"),
            {"email": "user@test.com", "password": "Incorrecta123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciales inválidas")
        self.assertContains(response, "value=\"user@test.com\"", html=False)
