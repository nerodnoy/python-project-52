from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    authorization_message = _('You are not authorized! Please, log in')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.authorization_message)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class AuthorRequiredMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        obj = self.get_object()
        # Проверяем, что текущий пользователь является автором задачи
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
