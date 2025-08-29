from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task details...'
            }),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class DependencyForm(forms.Form):
    prerequisite_task = forms.ModelChoiceField(
        queryset=Task.objects.none(),  # start empty, override in __init__
        label="Prerequisite Task"
    )
    group_type = forms.ChoiceField(
        choices=[
            ("ALL", "Required (All)"),
            ("ONE", "Required (One-of)"),
            ("OPT", "Optional")
        ],
        label="Dependency Type"
    )

    def __init__(self, *args, **kwargs):
        current_task = kwargs.pop("current_task", None)  # pass from view
        super().__init__(*args, **kwargs)

        if current_task:
            # Only allow choosing other tasks as prerequisites
            self.fields["prerequisite_task"].queryset = Task.objects.exclude(id=current_task.id)
        else:
            # fallback: all tasks
            self.fields["prerequisite_task"].queryset = Task.objects.all()
