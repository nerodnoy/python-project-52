from loguru import logger
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CrudUsersTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user_list_url = reverse('user_list')
        self.data_for_form = {
            'username': 'rodnoy',
            'first_name': 'Artyom',
            'last_name': 'Iliushin',
            'password1': 'W"q_uRe8p.x-~V>5jKMDUa',
            'password2': 'W"q_uRe8p.x-~V>5jKMDUa',
        }
        self.users_count_before_test = User.objects.count()

    def log_success(self, message):
        logger.info(message)

    def test_create_user(self):
        response = self.client.post(reverse('user_create'), self.data_for_form, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(User.objects.count(), self.users_count_before_test + 1)
        self.log_success("User successfully created.")

    def test_update_my_user(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(reverse('user_update', args=[2]), follow=True)
        self.assertEqual(response.status_code, 200)

        updated_data = self.data_for_form.copy()
        updated_data.update({'username': 'UserUpdated'})
        post_response = self.client.post(reverse('user_update', args=[2]), updated_data)
        self.assertRedirects(post_response, self.user_list_url)
        self.assertEqual(User.objects.get(pk=2).username, 'UserUpdated')
        self.log_success("User successfully updated.")

    def test_delete_my_user(self):
        user = User.objects.get(pk=1337)
        self.client.force_login(user)
        response = self.client.post(reverse('user_delete', args=[1337]), follow=True)
        self.assertRedirects(response, self.user_list_url)
        self.assertEqual(User.objects.count(), self.users_count_before_test - 1)
        self.log_success("User successfully deleted.")
