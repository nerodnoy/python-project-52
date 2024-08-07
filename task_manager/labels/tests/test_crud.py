from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status


class CrudLabelsTestCase(TestCase):
    fixtures = ['users.json', 'labels.json', 'tasks.json', 'statuses.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)  # Используем пользователя с ID 1
        self.client.force_login(self.user)
        self.label_list_url = reverse('label_list')
        self.label_create_url = reverse('label_create')
        self.label_update_url = lambda pk: reverse('label_update', args=[pk])
        self.label_delete_url = lambda pk: reverse('label_delete', args=[pk])
        self.login_url = reverse('login')

        self.new_label_data = {
            'name': 'Important'
        }
        self.updated_label_data = {
            'name': 'Very Important'
        }

    def test_label_list(self):
        response = self.client.get(self.label_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertContains(response, 'Bug')

    def test_create_label(self):
        response = self.client.post(self.label_create_url, self.new_label_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.label_list_url)
        self.assertTrue(Label.objects.filter(name='Important').exists())

    def test_update_label(self):
        label = Label.objects.get(pk=1)
        response = self.client.post(self.label_update_url(label.pk), self.updated_label_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.label_list_url)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Very Important')

    def test_delete_label(self):
        label = Label.objects.create(name='ToDelete')
        response = self.client.post(self.label_delete_url(label.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.label_list_url)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

    def test_delete_label_associated_with_task(self):
        label = Label.objects.create(name='Associated Label')
        status = Status.objects.get(pk=1)
        task = Task.objects.create(
            name='Task with Label',
            status=status,
            author=self.user,
            executor=self.user
        )
        task.label.add(label)

        response = self.client.post(self.label_delete_url(label.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.label_list_url)
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())

    def test_label_list_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.label_list_url)
        self.assertRedirects(response, self.login_url)

    def test_create_label_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.label_create_url, self.new_label_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_update_label_if_not_logged_in(self):
        self.client.logout()
        label = Label.objects.get(pk=1)
        response = self.client.post(self.label_update_url(label.pk), self.updated_label_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_delete_label_if_not_logged_in(self):
        self.client.logout()
        label = Label.objects.get(pk=1)
        response = self.client.post(self.label_delete_url(label.pk), follow=True)
        self.assertRedirects(response, self.login_url)
