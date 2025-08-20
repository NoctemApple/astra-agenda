from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='task_board'),
    path('add-task/', views.add_task, name='add_task'),
    path('add-dependency/', views.add_dependency, name='add_dependency'),
]
