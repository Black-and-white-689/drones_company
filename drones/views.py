from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.http import HttpResponseRedirect

from django.urls import reverse_lazy, reverse

from django.views import generic

from .models import Task, Worker, TaskType, Position

from .forms import (
    TaskForm,
    TaskSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerCreationForm,
)


#  Tasks
class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "drones/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("task_type").prefetch_related("assignees")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset.order_by("id")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "drones/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("drones:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("drones:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("drones:task-list")
