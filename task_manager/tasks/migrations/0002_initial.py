# Generated by Django 5.1 on 2024-08-09 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status', to='statuses.status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='tasklabelrelation',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labels.label'),
        ),
        migrations.AddField(
            model_name='tasklabelrelation',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task'),
        ),
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='label', through='tasks.TaskLabelRelation', to='labels.label', verbose_name='Labels'),
        ),
    ]
