from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "tasks/index.html")

def tasks(request):
    return render(request, "tasks/tasks.html")