from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Task,DependencyGroup, TaskDependency
from .forms import TaskForm, DependencyForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "tasks/index.html")

def tasks(request):
    return render(request, "tasks/tasks.html")

@login_required
def add_task(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        dependencies = request.POST.getlist('dependencies')  
        dependency_types = request.POST.getlist('dependency_types')

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()

            for dep_id, dep_type in zip(dependencies, dependency_types):
                group, _ = DependencyGroup.objects.get_or_create(
                    task=task,
                    group_type=dep_type
                )
                dep_task = Task.objects.get(id=dep_id, user=request.user)
                TaskDependency.objects.create(group=group, prerequisite_task=dep_task)

            return JsonResponse({'id': task.id, 'name': task.name, 'error': False})

        return JsonResponse({'error': True, 'messages': task_form.errors})