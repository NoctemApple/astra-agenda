from django import forms
from .models import Task, Dependency

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']

class DependencyForm(forms.ModelForm):
    class Meta:
        model = Dependency
        fields = ['target_task', 'prerequisite_task', 'group_id']
