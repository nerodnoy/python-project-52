from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from task_manager.mixins import UserPermissionMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/status_list.html'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')


class StatusUpdateView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')


class StatusDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):

    model = Status
    success_url = reverse_lazy('status_list')
    template_name = 'statuses/delete_status.html'

    protected_message = 'Status in use'
    protected_url = reverse_lazy('status_list')
