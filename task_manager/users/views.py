from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User
from ..mixins import AuthRequiredMixin, OwnerRequiredMixin, DeleteProtectionMixin


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    # SuccessMessageMixin:
    success_message = 'User created successfully!'

    extra_context = {
        'title': 'Create user',
        'button_name': 'Register',
    }


class UserUpdateView(AuthRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    # SuccessMessageMixin:
    success_message = 'User updated successfully!'

    # OwnerRequiredMixin:
    permission_message = 'You are not allowed to edit another user!'
    permission_url = reverse_lazy('user_list')

    extra_context = {
        'title': 'Update user',
        'button_name': 'Update',
    }


class UserDeleteView(AuthRequiredMixin, OwnerRequiredMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    # SuccessMessageMixin:
    success_message = 'User deleted successfully'

    # OwnerRequiredMixin:
    permission_message = 'You are not allowed to edit another user!'
    permission_url = reverse_lazy('user_list')

    # DeleteProtectionMixin:
    protected_message = 'Unable to delete a user because he is currently in use'
    protected_url = reverse_lazy('user_list')
