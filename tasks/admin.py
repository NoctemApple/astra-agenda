from django.contrib import admin
from .models import Task, DependencyGroup, TaskDependency

# Register your models here.

class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    extra = 1

@admin.register(DependencyGroup)
class DependencyGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "group_type")
    list_filter = ("group_type",)
    inlines = [TaskDependencyInline]

class DependencyGroupInline(admin.TabularInline):
    model = DependencyGroup
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "deadline", "completed", "created_at")
    search_fields = ("name", "description")
    list_filter = ("deadline", "completed")
    inlines = [DependencyGroupInline]

@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "prerequisite_task")

