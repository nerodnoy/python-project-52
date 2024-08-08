from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name=_('Name')
    )

    description = models.TextField(
        max_length=999,
        blank=True,
        verbose_name=_('Description')
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author')
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        related_name='executor',
        verbose_name=_('Executor')
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creation')
    )

    label = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        related_name='label',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
