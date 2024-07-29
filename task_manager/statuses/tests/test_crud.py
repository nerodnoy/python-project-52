from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.users.models import User


class CrudStatusesTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.status_list_url = reverse('status_list')
        self.status_create_url = reverse('status_create')
        self.status_update_url = lambda pk: reverse('status_update', args=[pk])
        self.status_delete_url = lambda pk: reverse('status_delete', args=[pk])
        self.login_url = reverse('login')
        self.client.force_login(self.user)
        self.new_status_data = {
            'name': 'Completed'
        }
        self.updated_status_data = {
            'name': 'Updated Status'
        }

    def test_status_list(self):
        response = self.client.get(self.status_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertContains(response, 'New')
        self.assertContains(response, 'In Progress')

    def test_create_status(self):
        response = self.client.post(self.status_create_url, self.new_status_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.status_list_url)
        self.assertTrue(Status.objects.filter(name='Completed').exists())

    def test_update_status(self):
        status = Status.objects.get(pk=1)
        response = self.client.post(self.status_update_url(status.pk), self.updated_status_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.status_list_url)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')

    def test_delete_status(self):
        status = Status.objects.get(pk=1)
        response = self.client.post(self.status_delete_url(status.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.status_list_url)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

    def test_create_status_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.status_create_url, self.new_status_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_update_status_if_not_logged_in(self):
        self.client.logout()
        status = Status.objects.get(pk=1)
        response = self.client.post(self.status_update_url(status.pk), self.updated_status_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_delete_status_if_not_logged_in(self):
        self.client.logout()
        status = Status.objects.get(pk=1)
        response = self.client.post(self.status_delete_url(status.pk), follow=True)
        self.assertRedirects(response, self.login_url)
