from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User
from ..mixins import AuthRequiredMixin, OwnerRequiredMixin


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    # flash-сообщение
    success_message = 'User created successfully!'

    extra_context = {
        'title': 'Create user',
        'button_name': 'Register',
    }


class UserUpdateView(AuthRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    extra_context = {
        'title': 'Update user',
        'button_name': 'Update',
    }


class UserDeleteView(AuthRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

