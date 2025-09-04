from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subtasks"
    )

    def __str__(self):
        return self.name

    def can_complete(self):
        """
        A task can be completed if all dependency groups are satisfied.
        - ALL: every prerequisite must be completed
        - ONE: at least one prerequisite must be completed
        - OPT: ignored for blocking
        """
        for group in self.dependency_groups.all():
            prereqs = [dep.prerequisite_task for dep in group.dependencies.all()]
            if group.group_type == "ALL":
                if not all(t.completed for t in prereqs):
                    return False
            elif group.group_type == "ONE":
                if not any(t.completed for t in prereqs):
                    return False
            elif group.group_type == "OPT":
                continue
        return True


class DependencyGroup(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependency_groups")

    GROUP_TYPE_CHOICES = [
        ("ALL", "Required (All)"),
        ("ONE", "Required (One-of)"),
        ("OPT", "Optional"),
    ]
    group_type = models.CharField(max_length=3, choices=GROUP_TYPE_CHOICES)

    def __str__(self):
        return f"{self.task.name} - {self.get_group_type_display()}"


class TaskDependency(models.Model):
    group = models.ForeignKey(DependencyGroup, on_delete=models.CASCADE, related_name="dependencies")
    prerequisite_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="dependent_links")

    def __str__(self):
        return f"{self.prerequisite_task.name} -> {self.group.task.name} ({self.group.group_type})"
