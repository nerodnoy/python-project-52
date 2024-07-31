from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.mixins import AuthRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'


class TaskCreateView(AuthRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    # success_message = 'Status created successfully'

    extra_context = {
        'title': 'Create task',
        'button_name': 'Create',
    }

    # Set current User as Author of Task
    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


# SuccessMessageMixin
class TaskUpdateView(AuthRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    # success_message = 'Status updated successfully'

    extra_context = {
        'title': 'Edit task',
        'button_name': 'Edit',
    }


# SuccessMessageMixin + DeleteProtectionMixin
class TaskDeleteView(AuthRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    # success_url = reverse_lazy('status_list')

    # SuccessMessageMixin:
    # success_message = 'Status deleted successfully'

    # DeleteProtectionMixin:
    # TO TEST:
    # protected_message = 'Can NOT delete task because it is currently in use'
    # protected_url = reverse_lazy('status_list')
