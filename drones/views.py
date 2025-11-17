from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from django.http import HttpResponseRedirect

from django.urls import reverse_lazy, reverse

from django.views import generic

from .models import Task, Worker, TaskType, Position

from django.shortcuts import render

from django.utils import timezone


from .forms import (
    TaskForm,
    TaskSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerCreationForm,
)


@login_required
def index(request):
    #  main_page

    #  Full date now
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    #  Done task in this month
    tasks_done_this_month = Task.objects.filter(
        is_done=True,
        deadline__year=current_year,
        deadline__month=current_month,
    )

    #  Full statistics
    num_workers = Worker.objects.count()
    num_tasks_total = Task.objects.count()
    num_tasks_done = Task.objects.filter(is_done=True).count()
    num_tasks_pending = Task.objects.filter(is_done=False).count()

    #  Visits
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks_total": num_tasks_total,
        "num_tasks_done": num_tasks_done,
        "num_tasks_pending": num_tasks_pending,
        "tasks_done_this_month": tasks_done_this_month,
        "current_month": now.strftime("%B"),
        "num_visits": num_visits + 1,
    }

    return render(request, "drones/index.html", context)


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
        queryset = super().get_queryset().select_related(
            "task_type").prefetch_related("assignees")
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


#  Workers
class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    template_name = "drones/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("position")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return queryset.order_by("id")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "drones/worker_detail.html"
    queryset = get_user_model().objects.prefetch_related("tasks__task_type")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    template_name = "drones/worker_form.html"
    success_url = reverse_lazy("drones:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("drones:worker-list")


#  Positions
class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "drones/position_list.html"
    context_object_name = "position_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset.order_by("id")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("drones:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("drones:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("drones:position-list")


#  Task_types
class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "drones/tasktype_list.html"
    context_object_name = "tasktype_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskTypeSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset.order_by("id")


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("drones:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("drones:tasktype-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("drones:tasktype-list")


@login_required
def toggle_assign_to_task(request, pk):
    worker = request.user
    task = Task.objects.get(pk=pk)

    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)

    return HttpResponseRedirect(reverse(
        "drones:task-detail", args=[pk])
    )
