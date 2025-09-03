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
from .forms import TaskForm

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


def index(request):
    tasks = Task.objects.filter(parent__isnull=True)  # only top-level
    return render(request, "tasks/index.html", {"tasks": tasks})

def help(request):
    return render(request, "tasks/help.html")

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

    # Provide existing tasks for dropdown (only top-level if you want cleaner)
    tasks = Task.objects.filter(user=request.user)
    tasks_json = json.dumps([{"id": t.id, "name": t.name} for t in tasks])

    return render(request, "tasks/add_task.html", {
        "form": form,
        "tasks_json": tasks_json,
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
    parent_task = get_object_or_404(Task, id=task_id, user=request.user)
    tasks = Task.objects.filter(user=request.user).exclude(id=parent_task.id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline") or None
        group_type = request.POST.get("group_type", "ALL")
        prereq_ids = request.POST.getlist("prereqs")

        if name:
            # 1. Create the subtask under parent
            new_task = Task.objects.create(
                name=name,
                description=description,
                deadline=deadline,
                parent=parent_task,   # ✅ nested correctly
                user=request.user
            )

            # 2. Create dependency group for this subtask
            group = DependencyGroup.objects.create(
                task=parent_task,
                group_type=group_type
            )

            # 3. Link selected prerequisites
            for prereq_id in prereq_ids:
                try:
                    prereq_task = Task.objects.get(id=prereq_id, user=request.user)
                    TaskDependency.objects.create(
                        group=group,
                        prerequisite_task=prereq_task
                    )
                except Task.DoesNotExist:
                    continue

            return redirect("task_detail", task_id=parent_task.id)

    return render(request, "tasks/add_dependency.html", {
        "task": parent_task,
        "tasks": tasks
    })


@login_required
def complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        if task.can_complete():
            task.completed = True
            task.save()
    return redirect("index")

