from loguru import logger
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class OwnerRequiredMixinTests(TestCase):
    fixtures = ['users.json']

    def log_success(self, message):
        logger.info(message)

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)

    def test_user_can_update_own_profile(self):
        response = self.client.get(reverse('user_update', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)
        self.log_success("User can update own profile.")

    def test_user_cannot_update_another_profile(self):
        response = self.client.get(reverse('user_update', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
        self.log_success("User can NOT update another profile.")

    def test_user_can_delete_own_profile(self):
        response = self.client.get(reverse('user_delete', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)
        self.log_success("User can delete own profile.")

    def test_user_cannot_delete_another_profile(self):
        response = self.client.get(reverse('user_delete', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
        self.log_success("User can NOT delete own profile.")
