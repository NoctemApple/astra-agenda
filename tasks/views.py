from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Task,DependencyGroup, TaskDependency
from .forms import TaskForm, DependencyForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tasks/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "tasks/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "tasks/register.html")


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('created_at')

    dependencies = []
    for task in tasks:
        for group in task.dependency_groups.all():
            for dep in group.dependencies.all():
                dependencies.append({
                    'prerequisite_task_id': dep.prerequisite_task.id,
                    'target_task_id': task.id,
                    'group_type': group.group_type
                })

    return render(request, 'tasks/index.html', {
        'tasks': tasks,
        'dependencies': dependencies
    })

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
                try:
                    dep_task = Task.objects.get(id=dep_id, user=request.user)
                except Task.DoesNotExist:
                    continue  # skip invalid IDs

                group, _ = DependencyGroup.objects.get_or_create(
                    task=task,
                    group_type=dep_type
                )
                TaskDependency.objects.create(group=group, prerequisite_task=dep_task)

            # AJAX or normal response
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'id': task.id, 'name': task.name, 'error': False})
            return redirect("index")

        return JsonResponse({'error': True, 'messages': task_form.errors})

    else:  # GET request
        tasks = Task.objects.filter(user=request.user)
        dependencies = TaskDependency.objects.filter(
            prerequisite_task__user=request.user
        ).values('prerequisite_task_id', 'group__task_id')

        return render(request, "tasks/add_task.html", {
            "tasks": tasks,
            "task_form": TaskForm(),
            "dependencies": list(dependencies)
        })




@login_required
def add_task_page(request):
    tasks = Task.objects.filter(user=request.user)
    dependencies = TaskDependency.objects.filter(prerequisite_task__user=request.user).values(
        'prerequisite_task_id', 'group__task_id'
    )
    return render(request, "add_task.html", {
        "tasks": tasks,
        "dependencies": list(dependencies)
    })
