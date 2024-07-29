from django import forms
from .models import Status


class StatusForm(forms.ModelForm):

    name = forms.CharField(
        max_length=150, required=True, label="name"
    )

    class Meta:
        model = Status
        fields = (
            'name',
        )
