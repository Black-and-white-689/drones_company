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
