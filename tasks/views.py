# astra/tasks/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Task, Dependency
from .forms import TaskForm, DependencyForm
import json

def index(request):
    tasks = Task.objects.all()
    dependencies = Dependency.objects.all()
    dependencies_json = json.dumps([
        {
            'id': dep.id,
            'target_task_id': dep.target_task.id,
            'prerequisite_task_id': dep.prerequisite_task.id,
            'group_id': dep.group_id
        }
        for dep in dependencies
    ])
    task_form = TaskForm()
    dependency_form = DependencyForm()
    return render(request, 'tasks/index.html', {
        'tasks': tasks,
        'dependencies_json': dependencies_json,
        'task_form': task_form,
        'dependency_form': dependency_form
    })

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return JsonResponse({'id': task.id, 'name': task.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_dependency(request):
    if request.method == "POST":
        form = DependencyForm(request.POST)
        if form.is_valid():
            dep = form.save()
            return JsonResponse({
                'id': dep.id,
                'target': dep.target_task.id,
                'prerequisite': dep.prerequisite_task.id,
                'group': dep.group_id
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)
