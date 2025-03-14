from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status

# Create your tests here.
class StatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.status = Status.objects.create(name='Test Status')

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses:status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        response = self.client.post(reverse('statuses:status_create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        response = self.client.post(reverse('statuses:status_update', args=[self.status.pk]), {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        response = self.client.post(reverse('statuses:status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())