from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import UserForm
from .models import User
from ..mixins import UserPermissionMixin


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')
