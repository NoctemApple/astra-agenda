from django.contrib import admin
from .models import Task, DependencyGroup, TaskDependency

class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    extra = 1

class DependencyGroupInline(admin.TabularInline):
    model = DependencyGroup
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "deadline", "completed")
    search_fields = ("name", "description")
    list_filter = ("deadline", "completed")
    # dependency groups show under Task inlines if you want
    inlines = [DependencyGroupInline]

class DependencyGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "group_type")
    inlines = [TaskDependencyInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(DependencyGroup, DependencyGroupAdmin)
admin.site.register(TaskDependency)
