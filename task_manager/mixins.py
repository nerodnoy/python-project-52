from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        # Тут переработать
        return HttpResponseRedirect(reverse('login'))
