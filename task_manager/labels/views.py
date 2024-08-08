from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from django.utils.translation import gettext as _


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')

    # SuccessMessageMixin:
    success_message = _('Label created successfully')

    extra_context = {
        'title': _('Create label'),
        'button_name': _('Create'),
    }


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')

    # SuccessMessageMixin:
    success_message = _('Label updated successfully')

    extra_context = {
        'title': _('Update label'),
        'button_name': _('Edit'),
    }


class LabelDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')

    # SuccessMessageMixin:
    success_message = _('Label deleted successfully')

    # DeleteProtectionMixin:
    protected_message = _('Can NOT delete label because it is associated with Task')
    protected_url = reverse_lazy('label_list')
