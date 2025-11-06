from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db.models import ForeignKey

from django.urls import reverse


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("drones:worker-detail", kwargs={"pk": self.pk})

    @property
    def done_tasks_count(self):
        # Done tasks
        return self.task.filter(is_done=True).count()

    @property
    def pending_tasks_count(self):
        # Undone tasks
        return self.task.filter(is_done=False).count()
