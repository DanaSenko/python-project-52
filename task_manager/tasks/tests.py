from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

from .models import Task


class TestTask(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.other_user = User.objects.create_user(
            username='other', password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.status = Status.objects.create(name='Test Status')  # type: ignore
        self.task = Task.objects.create(  # type: ignore
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user,
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(
            reverse('tasks:task_create'),
            {
                'name': 'Task New',
                'description': 'New Description',
                'status': self.status.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Task New').exists())  # type: ignore

    def test_task_create_invalid_data(self):
        response = self.client.post(
            reverse('tasks:task_create'),
            {
                'name': '',  # Invalid: empty name
                'status': self.status.id,
            },
        )
        self.assertEqual(response.status_code, 200)  # Returns to form
        self.assertFalse(Task.objects.filter(name='').exists())

    def test_task_update_view(self):
        self.client.login(username='author', password='testpass123')

        response = self.client.post(
            reverse('tasks:task_update', args=[self.task.pk]),
            {
                'name': 'Task Updated',
                'description': 'Updated Description',
                'status': self.status.pk,  # Use PK instead of name
            },
        )

        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful update
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Task Updated')

    def test_task_delete_view(self):
        response = self.client.post(
            reverse('tasks:task_delete', args=[self.task.pk])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful deletion
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        self.client.login(username='other', password='12345')

        response = self.client.post(
            reverse('tasks:task_delete', args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
