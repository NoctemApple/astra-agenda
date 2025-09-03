from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Task.objects.all(),
        required=False,
        empty_label="(No parent – top-level task)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task details...'
            }),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
