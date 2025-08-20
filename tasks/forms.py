from django import forms
from .models import Task, DependencyGroup, TaskDependency

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline']

class DependencyForm(forms.Form):
    prerequisite_task = forms.ModelChoiceField(
        queryset=None,
        label="Select Task"
    )
    group_type = forms.ChoiceField(
        choices=[
            ("ALL", "Required (All)"),
            ("ONE", "Required (One-of)"),
            ("OPT", "Optional")
        ],
        label="Dependency Type"
    )
    
