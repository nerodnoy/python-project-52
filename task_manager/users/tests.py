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

    def test_user_list(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_create(self):
        response = self.client.post(
            reverse('user_create'), self.data_for_form, follow=True
        )
        self.assertRedirects(response, self.login_url)
        self.assertEqual(User.objects.count(), self.users_count_before_test + 1)

    def test_user_update_mine(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.get(reverse('user_update', args=[2]), follow=True)
        self.assertEqual(response.status_code, 200)

        updated_data = self.data_for_form.copy()
        updated_data.update({'username': 'UserUpdated'})
        post_response = self.client.post(reverse('user_update', args=[2]), updated_data)
        self.assertRedirects(post_response, self.user_list_url)
        self.assertEqual(User.objects.get(pk=2).username, 'UserUpdated')

    def test_user_delete_mine(self):
        user = User.objects.get(pk=1337)
        self.client.force_login(user)
        response = self.client.post(reverse('user_delete', args=[1337]), follow=True)
        self.assertRedirects(response, self.user_list_url)
        self.assertEqual(User.objects.count(), self.users_count_before_test - 1)


class OwnerRequiredMixinTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)

    def test_user_can_update_own_profile(self):
        response = self.client.get(reverse('user_update', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_update_another_profile(self):
        response = self.client.get(reverse('user_update', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)

    def test_user_can_delete_own_profile(self):
        response = self.client.get(reverse('user_delete', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_delete_another_profile(self):
        response = self.client.get(reverse('user_delete', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
