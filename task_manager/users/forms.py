from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'usable_password' in self.fields:
            del self.fields['usable_password']

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )
