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
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("index")
    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {
        "form": form
    })

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    dependency_groups = task.dependency_groups.prefetch_related("dependencies__prerequisite_task")

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "dependency_groups": dependency_groups
    })


@login_required
def add_dependency(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

    if request.method == "POST":
        form = DependencyForm(request.POST)
        form.fields["prerequisite_task"].queryset = Task.objects.filter(user=request.user).exclude(id=task.id)

        if form.is_valid():
            prerequisite_task = form.cleaned_data["prerequisite_task"]
            group_type = form.cleaned_data["group_type"]

            # Create/find dependency group
            group, _ = DependencyGroup.objects.get_or_create(task=task, group_type=group_type)
            TaskDependency.objects.create(group=group, prerequisite_task=prerequisite_task)

            return redirect("task_detail", task_id=task.id)
    else:
        form = DependencyForm()
        form.fields["prerequisite_task"].queryset = Task.objects.filter(user=request.user).exclude(id=task.id)

    return render(request, "tasks/add_dependency.html", {
        "task": task,
        "form": form
    })
