from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from task_manager.mixins import AuthRequiredMixin, OwnerRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = 'Task created successfully'

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
class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = 'Task edited successfully'

    extra_context = {
        'title': 'Edit task',
        'button_name': 'Edit',
    }


class TaskDeleteView(AuthRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')

    # SuccessMessageMixin:
    success_message = 'Task deleted successfully'

    # OwnerRequiredMixin:
    permission_message = "The task can be deleted by its' author only"
    permission_url = reverse_lazy('task_list')
