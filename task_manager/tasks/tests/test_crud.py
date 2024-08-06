from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status


class CrudTasksTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        self.author = User.objects.get(pk=1)
        self.another_user = User.objects.get(pk=2)
        self.task_list_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task_update_url = lambda pk: reverse('task_update', args=[pk])
        self.task_delete_url = lambda pk: reverse('task_delete', args=[pk])
        self.login_url = reverse('login')
        self.client.force_login(self.author)

        self.new_task_data = {
            'name': 'New Task',
            'description': 'This is a new task',
            'status': Status.objects.first().pk,
            'executor': self.author.pk,
        }

        self.updated_task_data = {
            'name': 'Updated Task',
            'description': 'This is an updated task',
            'status': Status.objects.first().pk,
            'executor': self.author.pk,
        }

    def test_task_list(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_create_task(self):
        response = self.client.post(self.task_create_url, self.new_task_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.task_list_url)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_update_task(self):
        task = Task.objects.get(pk=1)
        response = self.client.post(self.task_update_url(task.pk), self.updated_task_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.task_list_url)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')

    def test_delete_task_by_author(self):
        task = Task.objects.create(
            name='Task to Delete',
            description='This task will be deleted',
            status=Status.objects.first(),
            author=self.author,  # Убедитесь, что задача принадлежит текущему пользователю
            executor=self.author
        )
        response = self.client.post(self.task_delete_url(task.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.task_list_url)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_delete_task_by_non_author(self):
        self.client.force_login(self.another_user)
        task = Task.objects.create(
            name='Task that should not be deleted',
            description='Only author can delete this',
            status=Status.objects.first(),
            author=self.author,
            executor=self.author
        )
        response = self.client.post(self.task_delete_url(task.pk), follow=True)
        self.assertRedirects(response, self.task_list_url)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

    def test_create_task_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.task_create_url, self.new_task_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_update_task_if_not_logged_in(self):
        self.client.logout()
        task = Task.objects.get(pk=1)
        response = self.client.post(self.task_update_url(task.pk), self.updated_task_data, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_delete_task_if_not_logged_in(self):
        self.client.logout()
        task = Task.objects.get(pk=1)
        response = self.client.post(self.task_delete_url(task.pk), follow=True)
        self.assertRedirects(response, self.login_url)
