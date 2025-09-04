from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("help/", views.help, name="help"),
    path("add/", views.add_task, name="add_task"),
    path("complete/<int:task_id>/", views.complete, name="complete"),


    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/add_dependency/", views.add_dependency, name="add_dependency"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),


    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

]