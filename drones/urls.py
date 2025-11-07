from django.urls import path

from .views import (
    index,
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
    path("", index, name="index"),
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
    #  Positions
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    #  Task-types
    path(
        "tasktypes/",
        TaskTypeListView.as_view(),
        name="tasktype-list"
    ),
    path(
        "tasktypes/create/",
        TaskTypeCreateView.as_view(),
        name="tasktype-create"
    ),
    path(
        "tasktypes/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="tasktype-update"
    ),
    path(
        "tasktypes/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="tasktype-delete"
    ),
]
