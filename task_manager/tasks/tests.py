from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from task_manager.statuses.models import Status


class TestTask(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.status = Status.objects.create(name="Test Status")
        self.task = Task.objects.create(
            name="Test Task", status=self.status, author=self.user
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_create_view(self):
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "name": "Task New",
                "description": "New Description",
                "status": self.status.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Task New").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.pk]),
            {
                "name": "Task Updated",
                "description": "Updated Description",
                "status": self.status.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Task Updated")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("tasks:task_delete", args=[self.task.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="Test Task").exists())
