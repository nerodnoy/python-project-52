from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')

    # SuccessMessageMixin:
    success_message = _('Status created successfully')

    extra_context = {
        'title': _('Create status'),
        'button_name': _('Create'),
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')

    # SuccessMessageMixin:
    success_message = _('Status updated successfully')

    extra_context = {
        'title': _('Update status'),
        'button_name': _('Edit'),
    }


class StatusDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')

    # SuccessMessageMixin:
    success_message = _('Status deleted successfully')

    # DeleteProtectionMixin:
    protected_message = _('Can NOT delete status because it is currently in use')
    protected_url = reverse_lazy('status_list')
