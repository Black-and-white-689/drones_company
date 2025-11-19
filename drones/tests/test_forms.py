from django.test import TestCase

from django.contrib.auth import get_user_model

from drones.forms import (TaskForm,
                          WorkerCreationForm,
                          TaskSearchForm,
                          WorkerSearchForm,
                          PositionSearchForm,
                          TaskTypeSearchForm)

from drones.models import TaskType, Position


class TestForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="12345")
        self.position = Position.objects.create(name="Engineer")
        self.task_type = TaskType.objects.create(name="Testing")

    def test_task_form_valid(self):
        form_data = {
            "name": "Task 1",
            "description": "Description",
            "deadline": "2025-12-31",
            "is_done": False,
            "priority": "Medium",
            "task_type": self.task_type.pk,
            "assignees": [self.user.pk]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "newuser",
            "password1": "Complexpass123",
            "password2": "Complexpass123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "position": self.position.pk
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_forms(self):
        for FormClass in [TaskSearchForm, WorkerSearchForm, PositionSearchForm, TaskTypeSearchForm]:
            form = FormClass(data={"q": "test"})
            self.assertTrue(form.is_valid())
