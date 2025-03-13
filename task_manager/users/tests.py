from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserTests(TestCase):
    """Build new user before each test"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_user_create(self):
        response = self.client.post(
            reverse("create_user"),
            {
                "username": "newuser",
                "password1": "complexpassword123",
                "password2": "complexpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("update_user", args=[self.user.pk]),
            {
                "username": "updateduser",
                "first_name": "updated",
                "last_name": "user",
                "password": "newpassword",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("delete_user", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)  # Редирект после успешного удаления
