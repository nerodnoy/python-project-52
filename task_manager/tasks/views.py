from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django_filters.views import FilterView
from task_manager.mixins import AuthRequiredMixin, AuthorRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import User
from django.utils.translation import gettext as _


class TaskDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskFilterView(AuthRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'

    extra_context = {
        'button_name': _('Show'),
    }


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = _('Task created successfully')

    extra_context = {
        'title': _('Create task'),
        'button_name': _('Create'),
    }

    # Set current User as Author of Task
    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


# SuccessMessageMixin
class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = _('Task edited successfully')

    extra_context = {
        'title': _('Edit task'),
        'button_name': _('Edit'),
    }


class TaskDeleteView(AuthRequiredMixin, AuthorRequiredMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = _('Task deleted successfully')

    # AuthorRequiredMixin:
    permission_message = _("The task can be deleted by its' author only")
    permission_url = reverse_lazy('task_list')
