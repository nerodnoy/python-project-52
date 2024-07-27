from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User
from ..mixins import AuthRequiredMixin


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    extra_context = {
        'title': 'Create user',
        'button_name': 'Register',
    }


# Добавить UserPermission
class UserUpdateView(AuthRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    extra_context = {
        'title': 'Update user',
        'button_name': 'Update',
    }


# Добавить UserPermission
class UserDeleteView(AuthRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

