from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    target_task = models.ForeignKey(Task, related_name='dependencies', on_delete=models.CASCADE)
    prerequisite_task = models.ForeignKey(Task, related_name='unlocks', on_delete=models.CASCADE)
    group_id = models.IntegerField(default=1)  
    # group_id allows OR logic: tasks in the same group_id mean "ANY of these can unlock target_task"

    def __str__(self):
        return f"{self.prerequisite_task} → {self.target_task} (Group {self.group_id})"
