from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для изменения другого пользователя.")
