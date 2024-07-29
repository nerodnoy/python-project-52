from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'


class StatusCreateView(AuthRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')

    extra_context = {
        'title': 'Create status',
        'button_name': 'Create',
    }


class StatusUpdateView(AuthRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')

    extra_context = {
        'title': 'Update status',
        'button_name': 'Update',
    }


class StatusDeleteView(AuthRequiredMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('status_list')
    template_name = 'statuses/status_delete.html'
