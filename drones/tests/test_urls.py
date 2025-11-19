from django.test import TestCase

from django.urls import reverse, resolve

from drones.views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    ToggleAssignToTaskView,
)

class TestUrls(TestCase):
    def test_index_url(self):
        url = reverse("drones:index")
        resolved = resolve(url)
        self.assertEqual(resolved.func, index)

    def test_cbv_urls(self):
        cbv_urls = [
            ("task-list", TaskListView, False),
            ("task-detail", TaskDetailView, True),
            ("task-create", TaskCreateView, False),
            ("task-update", TaskUpdateView, True),
            ("task-delete", TaskDeleteView, True),
            ("worker-list", WorkerListView, False),
            ("worker-detail", WorkerDetailView, True),
            ("worker-create", WorkerCreateView, False),
            ("worker-delete", WorkerDeleteView, True),
            ("position-list", PositionListView, False),
            ("position-create", PositionCreateView, False),
            ("position-update", PositionUpdateView, True),
            ("position-delete", PositionDeleteView, True),
            ("tasktype-list", TaskTypeListView, False),
            ("tasktype-create", TaskTypeCreateView, False),
            ("tasktype-update", TaskTypeUpdateView, True),
            ("tasktype-delete", TaskTypeDeleteView, True),
            ("task-toggle-assign", ToggleAssignToTaskView, True),
        ]
        for name, view_class, requires_pk in cbv_urls:
            url = reverse(f"drones:{name}", args=[1] if requires_pk else None)
            resolved = resolve(url)
            self.assertEqual(resolved.func.view_class, view_class)
