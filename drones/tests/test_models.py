from django.test import TestCase

from django.contrib.auth import get_user_model

from drones.models import Task, TaskType, Position

class TestModels(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Engineer")
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            password="12345",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Testing")
        self.task_done = Task.objects.create(
            name="Done Task",
            task_type=self.task_type,
            is_done=True
        )
        self.task_done.assignees.add(self.worker)
        self.task_pending = Task.objects.create(
            name="Pending Task",
            task_type=self.task_type,
            is_done=False
        )
        self.task_pending.assignees.add(self.worker)

    def test_worker_done_tasks_count(self):
        self.assertEqual(self.worker.done_tasks_count, 1)

    def test_worker_pending_tasks_count(self):
        self.assertEqual(self.worker.pending_tasks_count, 1)

    def test_worker_get_absolute_url(self):
        url = self.worker.get_absolute_url()
        self.assertIn(str(self.worker.pk), url)

    def test_worker_str(self):
        self.assertIn("testuser", str(self.worker))
        self.assertIn("Engineer", str(self.worker))

    def test_position_worker_count(self):
        self.assertEqual(self.position.worker_count(), 1)

    def test_position_str(self):
        self.assertEqual(str(self.position), "Engineer")

    def test_task_str(self):
        self.assertIn("Done Task", str(self.task_done))
        self.assertIn("Is done", str(self.task_done))
        self.assertIn("Pending Task", str(self.task_pending))
        self.assertIn("In progress", str(self.task_pending))

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Testing")
