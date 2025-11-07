from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db.models import ForeignKey

from django.urls import reverse


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.PROTECT,
        verbose_name="Position",
        blank=True,
        null=True)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return (f"{self.username}: ({self.first_name} {self.last_name}, "
                f"Position: {self.position})")

    def get_absolute_url(self):
        return reverse("drones:worker-detail", kwargs={"pk": self.pk})

    @property
    def done_tasks_count(self):
        # Done tasks
        return self.tasks.filter(is_done=True).count()

    @property
    def pending_tasks_count(self):
        # Undone tasks
        return self.tasks.filter(is_done=False).count()


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent"
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    name = models.CharField(max_length=255, verbose_name="Task_name")
    description = models.TextField(blank=True, null=True, verbose_name="Task_description")
    deadline = models.DateField(verbose_name="Deadline", null=True, blank=True)
    is_done = models.BooleanField(default=False, verbose_name="Done")
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Priority"
    )
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        verbose_name="worker",
    )

    def __str__(self):
        return f"{self.name} ({'Is done' if self.is_done else 'In progress'})"


class TaskType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Task_type_name")

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Position_name")

    def __str__(self):
        return self.name
