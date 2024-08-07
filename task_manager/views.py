from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home')

    # SuccessMessageMixin:
    success_message = 'You are logged in'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    # Logout flash-message manually created
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You are logged out')
        return super().dispatch(request, *args, **kwargs)
