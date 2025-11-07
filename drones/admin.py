from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Worker, Task, TaskType, Position


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("name", "is_done", "priority", "deadline")
    readonly_fields = ("name", "is_done", "priority", "deadline")
    show_change_link = True


#  Custom for Worker
@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
        "is_staff",
        "done_tasks_count",
        "pending_tasks_count",
    )
    list_filter = ("position", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional information",
            {
                "fields": ("position",),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                ),
            },
        ),
    )

    def done_tasks_count(self, obj):
        return obj.done_tasks_count
    done_tasks_count.short_description = "Done tasks"

    def pending_tasks_count(self, obj):
        return obj.pending_tasks_count
    pending_tasks_count.short_description = "Pending tasks"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "is_done",
        "deadline",
        "display_assignees",
    )
    list_filter = (
        "is_done",
        "priority",
        "task_type",
        "assignees__position",
    )
    search_fields = ("name", "description", "task_type__name", "assignees__username")
    date_hierarchy = "deadline"
    ordering = ("-deadline",)
    filter_horizontal = ("assignees",)

    def display_assignees(self, obj):
        return ", ".join([worker.username for worker in obj.assignees.all()])
    display_assignees.short_description = "Workers"


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "task_count")
    search_fields = ("name",)
    inlines = [TaskInline]

    def task_count(self, obj):
        return obj.task_count()
    task_count.short_description = "Number of tasks"


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "worker_count")
    search_fields = ("name",)
    inlines = [TaskInline]

    def worker_count(self, obj):
        return obj.worker_count()
    worker_count.short_description = "Number of workers"