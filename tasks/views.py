from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.urls import reverse
from django.utils.safestring import mark_safe
import json

from .models import Task, DependencyGroup, TaskDependency
from .forms import TaskForm


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
    tasks = Task.objects.filter(parent__isnull=True)
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

    # Provide existing tasks for dropdown
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

    if request.method == "POST":
        # Get task details
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        group_type = request.POST.get("group_type", "ALL")

        # Create the new prerequisite task as a subtask of parent_task
        prereq_task = Task.objects.create(
            user=request.user,
            name=name,
            description=description,
            parent=parent_task   # 👈 ensures hierarchy
        )

        # Create/find dependency group
        group, created = DependencyGroup.objects.get_or_create(
            task=parent_task,
            group_type=group_type
        )

        # Link prerequisite to the parent task
        TaskDependency.objects.get_or_create(
            group=group,
            prerequisite_task=prereq_task
        )

        return redirect("task_detail", task_id=parent_task.id)

    return render(request, "tasks/add_dependency.html", {
        "task": parent_task
    })


@login_required
def complete(request, task_id):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        task = get_object_or_404(Task, id=task_id)

        if not task.completed:
            incomplete_info = task.incomplete_dependencies()
            if incomplete_info: 
                return JsonResponse({
                    "task_id": task.id,
                    "completed": False,
                    "error": f"Cannot complete '{task.name}'.",
                    "incomplete_dependencies": incomplete_info
                }, status=400)
            else:
                task.completed = True
                task.save()
                return JsonResponse({"task_id": task.id, "completed": True})
        else:
            # Undo / cancel
            task.completed = False
            task.save()
            return JsonResponse({"task_id": task.id, "completed": False})

    return JsonResponse({"error": "Invalid request"}, status=400)





@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()  # cascades to subtasks
        return redirect("index")
