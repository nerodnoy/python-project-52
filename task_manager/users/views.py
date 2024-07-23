from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import UserRegister, UserUpdate
from .models import User


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    form_class = UserRegister
    template_name = 'users/user_form.html'
    success_url = '/'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdate
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        return self.request.user
