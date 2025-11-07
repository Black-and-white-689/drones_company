from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Worker, Task, TaskType, Position


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("name", "is_done", "priority", "deadline")
    readonly_fields = ("name", "is_done", "priority", "deadline")
    show_change_link = True
