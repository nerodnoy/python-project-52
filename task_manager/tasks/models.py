from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


# Create your models here.
class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )

    description = models.TextField(
        max_length=999,
        blank=True,
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
    )

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    label = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        related_name='label',
    )

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
