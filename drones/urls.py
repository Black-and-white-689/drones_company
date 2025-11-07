from django.urls import path

from .views import (
TaskListView,
TaskDetailView,
TaskCreateView,
TaskDeleteView,
TaskUpdateView,
WorkerListView,
WorkerDetailView,
WorkerCreateView,
WorkerDeleteView,
PositionListView,
PositionCreateView,
PositionDeleteView,
PositionUpdateView,
TaskTypeListView,
TaskTypeCreateView,
TaskTypeUpdateView,
TaskTypeDeleteView,
toggle_assign_to_task,
)


app_name = "drones"


urlpatterns = [
    #  Tasks
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="task-toggle-assign"
    ),
    #  Workers
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
]