import django_filters
from django import forms
from django_filters import ModelChoiceFilter, BooleanFilter
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):
    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    # Показать мои задачи
    personal_tasks = BooleanFilter(
        label=_('Get personal tasks'),
        widget=forms.CheckboxInput,
        method='get_personal_tasks',
    )

    def get_personal_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']
