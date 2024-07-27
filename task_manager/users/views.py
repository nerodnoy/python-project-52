from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User


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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    # LoginRequiredMixin возможности:
    # если не авторизован, то перенаправляем на /login/

    # login_url = reverse_lazy('login')

    extra_context = {
        'title': 'Update user',
        'button_name': 'Update',
    }


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    # LoginRequiredMixin возможности:
    # если не авторизован, то перенаправляем на /login/

    # login_url = reverse_lazy('login')

# AuthRequired
# PermissionRequired
