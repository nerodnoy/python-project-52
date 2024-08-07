from django import forms
from .models import Label


class LabelForm(forms.ModelForm):

    name = forms.CharField(
        max_length=150, required=True, label="name"
    )

    class Meta:
        model = Label
        fields = (
            'name',
        )
