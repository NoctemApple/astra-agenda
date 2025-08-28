from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

import json


from .models import Task, DependencyGroup, TaskDependency
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
    tasks = Task.objects.filter(user=request.user).order_by("created_at")

    for task in tasks:
        task.has_unmet_dependencies = not task.can_complete()

    return render(request, "tasks/index.html", {
        "tasks": tasks,
    })


def tasks(request):
    return render(request, "tasks/tasks.html")

@login_required
def add_task(request):
    if request.method == "GET":
        form = TaskForm()
        tasks = Task.objects.filter(user=request.user).order_by('created_at')
        tasks_json = json.dumps(list(tasks.values("id", "name")))
        return render(request, "tasks/add_task.html", {
            "form": form,
            "tasks": tasks,
            "tasks_json": mark_safe(tasks_json)
        })

    elif request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("index") 
        else:
            # If invalid, re-render the form with errors
            tasks = Task.objects.filter(user=request.user).order_by('created_at')
            tasks_json = json.dumps(list(tasks.values("id", "name")))
            return render(request, "tasks/add_task.html", {
                "form": form,
                "tasks": tasks,
                "tasks_json": mark_safe(tasks_json)
            })



@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    dependency_groups = task.dependency_groups.prefetch_related("dependencies__prerequisite_task")
    return render(request, "tasks/task_detail.html", {
        "task": task,
        "dependency_groups": dependency_groups
    })


@login_required
def add_dependency(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = DependencyForm(request.POST)
        form.fields["prerequisite_task"].queryset = Task.objects.filter(user=request.user).exclude(id=task.id)

        if form.is_valid():
            prerequisite_task = form.cleaned_data["prerequisite_task"]
            group_type = form.cleaned_data["group_type"]
            group, _ = DependencyGroup.objects.get_or_create(task=task, group_type=group_type)
            TaskDependency.objects.create(group=group, prerequisite_task=prerequisite_task)
            return redirect("task_detail", task_id=task.id)
    else:
        form = DependencyForm()
        form.fields["prerequisite_task"].queryset = Task.objects.filter(user=request.user).exclude(id=task.id)

    return render(request, "tasks/add_dependency.html", {"task": task, "form": form})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        if task.can_complete():
            task.completed = True
            task.save()
    return redirect("index")

