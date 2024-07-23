from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserRegister(UserCreationForm):
    class Meta:

        model = User

        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class UserUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
