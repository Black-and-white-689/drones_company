from django.test import TestCase

from django.urls import reverse

from django.contrib.auth import get_user_model

from django.utils import timezone

from drones.models import Task, TaskType, Position

User = get_user_model()

class BaseSetupMixin:
    def setUp(self):
        self.position = Position.objects.create(name="Engineer")
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            position=self.position
        )
        self.client.login(username="testuser", password="password123")
        self.task_type = TaskType.objects.create(name="Testing")
        self.task_done = Task.objects.create(
            name="Done Task",
            task_type=self.task_type,
            is_done=True,
            deadline=timezone.now().date()
        )
        self.task_done.assignees.add(self.user)
        self.task_pending = Task.objects.create(
            name="Pending Task",
            task_type=self.task_type,
            is_done=False,
            deadline=timezone.now().date()
        )


# Index
class IndexViewTests(BaseSetupMixin, TestCase):
    def test_index_accessible_and_context(self):
        response = self.client.get(reverse("drones:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_workers", response.context)
        self.assertIn("tasks_done_this_month", response.context)
        self.assertEqual(response.context["num_workers"], 1)
        self.assertEqual(response.context["num_tasks_total"], 2)
        self.assertEqual(response.context["num_tasks_done"], 1)
        self.assertEqual(response.context["num_tasks_pending"], 1)
        self.assertEqual(response.context["num_visits"], 1)


# Task
class TaskViewsTests(BaseSetupMixin, TestCase):
    def test_task_list_view(self):
        response = self.client.get(reverse("drones:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_list", response.context)
        self.assertIn("search_form", response.context)
        self.assertEqual(len(response.context["task_list"]), 2)

    def test_task_detail_view(self):
        response = self.client.get(reverse("drones:task-detail", args=[self.task_done.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_done.name)

    def test_task_create_update_delete_views(self):
        # Create
        response = self.client.post(
            reverse("drones:task-create"),
            {
                "name": "New Task",
                "task_type": self.task_type.pk,
                "is_done": False,
                "priority": "Medium",
                "assignees": [self.user.pk],
            }
        )
        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(name="New Task")
        self.assertIn(self.user, new_task.assignees.all())

        # Update
        response = self.client.post(
            reverse("drones:task-update", args=[new_task.pk]),
            {
                "name": "Updated Task",
                "task_type": self.task_type.pk,
                "is_done": True,
                "priority": "High",
                "assignees": [self.user.pk],
            }
        )
        self.assertEqual(response.status_code, 302)
        new_task.refresh_from_db()
        self.assertEqual(new_task.name, "Updated Task")
        self.assertTrue(new_task.is_done)

        # Delete
        response = self.client.post(reverse("drones:task-delete", args=[new_task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=new_task.pk).exists())


# Worker
class WorkerViewsTests(BaseSetupMixin, TestCase):
    def test_worker_list_view(self):
        response = self.client.get(reverse("drones:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("worker_list", response.context)
        self.assertIn("search_form", response.context)
        self.assertEqual(len(response.context["worker_list"]), 1)

    def test_worker_detail_view(self):
        response = self.client.get(reverse("drones:worker-detail", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_worker_create_delete_views(self):
        # Create
        response = self.client.post(
            reverse("drones:worker-create"),
            {
                "username": "newworker",
                "password1": "strongpass123",
                "password2": "strongpass123",
                "position": self.position.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        new_worker = User.objects.get(username="newworker")
        self.assertEqual(new_worker.position, self.position)

        # Delete
        response = self.client.post(reverse("drones:worker-delete", args=[new_worker.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="newworker").exists())


# Position
class PositionViewsTests(BaseSetupMixin, TestCase):
    def test_position_list_view(self):
        response = self.client.get(reverse("drones:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("position_list", response.context)
        self.assertIn("search_form", response.context)

    def test_position_create_update_delete_views(self):
        # Create
        response = self.client.post(reverse("drones:position-create"), {"name": "Manager"})
        self.assertEqual(response.status_code, 302)
        pos = Position.objects.get(name="Manager")

        # Update
        response = self.client.post(reverse("drones:position-update", args=[pos.pk]), {"name": "Lead"})
        self.assertEqual(response.status_code, 302)
        pos.refresh_from_db()
        self.assertEqual(pos.name, "Lead")

        # Delete
        response = self.client.post(reverse("drones:position-delete", args=[pos.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(pk=pos.pk).exists())


# TaskType Views
class TaskTypeViewsTests(BaseSetupMixin, TestCase):
    def test_tasktype_list_view(self):
        response = self.client.get(reverse("drones:tasktype-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasktype_list", response.context)
        self.assertIn("search_form", response.context)

    def test_tasktype_create_update_delete_views(self):
        # Create
        response = self.client.post(reverse("drones:tasktype-create"), {"name": "Bug"})
        self.assertEqual(response.status_code, 302)
        tt = TaskType.objects.get(name="Bug")

        # Update
        response = self.client.post(reverse("drones:tasktype-update", args=[tt.pk]), {"name": "Feature"})
        self.assertEqual(response.status_code, 302)
        tt.refresh_from_db()
        self.assertEqual(tt.name, "Feature")

        # Delete
        response = self.client.post(reverse("drones:tasktype-delete", args=[tt.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(pk=tt.pk).exists())


# ToggleAssign
class ToggleAssignViewTests(BaseSetupMixin, TestCase):
    def test_toggle_assign_add_and_remove(self):
        url = reverse("drones:task-toggle-assign", args=[self.task_pending.pk])
        # Initially not assigned
        self.assertNotIn(self.user, self.task_pending.assignees.all())

        # POST should add
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.task_pending.refresh_from_db()
        self.assertIn(self.user, self.task_pending.assignees.all())

        # POST again should remove
        resp = self.client.post(url)
        self.task_pending.refresh_from_db()
        self.assertNotIn(self.user, self.task_pending.assignees.all())

    def test_toggle_assign_get_not_allowed(self):
        url = reverse("drones:task-toggle-assign", args=[self.task_pending.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)
