from django.urls import path
from .filters import TaskFilter
from .views import (TaskCreateView, TaskUpdateView, TaskDeleteView,
                    TaskDetailView, TaskFilterView)

urlpatterns = [
    path('', TaskFilterView.as_view(filterset_class=TaskFilter), name='task_list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
