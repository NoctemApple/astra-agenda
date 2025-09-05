# Astra Agenda

## Description

This is a task management application built with Django; that focuses on creating tasks with prerequirements that ensure the user can navigate the intricacies of their objectives with subtasks of various requirements, that vary from all, one, or optional.

### Additional information

This application was actually inspired by a task app I use for myself but I always found myself constantly chaining tasks in real life, and thats where the main idea for the application.

Because the application is also a web application, aside from being a literal requirement by CS50w it is mobile responsive thanks to bootstrap which makes it viable for use though admittedly there is some jankiness with the subsubtasks the problem is too minor to dedicate more time.

The name is an attempt to imitate the naming conventions of the Imperium of Man from Warhammer 40k, where Astra and Agenda are latin for "stars" and Agenda means "list" (according to google translate) respectively.

## Distinctiveness and Complexity

### Distinctiveness 

This app bears no similarities in terms of functionality to previous CS50W projects but some of the codes and structure are taken from previous projects namely the use of layout.html, and the login/logout/register.

Astra Agenda is distinct from other task applications because of the dependency system which encourages a quest like system similar to those found in video games.

While it is inspired from the quest system, gamification isn't implemented. (Mostly due to it being overkill, and the creator not being a fan of gamification)

### Complexity

As for complexity the appication focuses on dependencies with three rules:

- All which requires completing ALL
- ONE can be done by accomplishing one of the tasks
- OPT has no bearing on completion status

Additionally we include nested subtasks while they can only cover two levels of subtasks this is considered sufficient as more sub levels is uneccessary.

Adding to the complexity are the models, and tasks to dependency relationships.

As for the UI it namely used bootstrap/Javascript for designing the UI like the accordions, floating buttons, and overall appearance of the application.

Additionally bootstrap makes the application mobile responsive.

## File Contents

manage.py   -> standard file for running commands.
.gitignore  -> namely to ignore database, and os specifics cache.

### tasks/
admin.py    -> register models, and allows access to admin powers
models.py   -> models for Tasks, and Dependency
views.py    -> logic for rendering tasks, handling the backend, and dependencies
urls.py     -> for the url patterns that create a map for the buttons.
forms.py    -> hold form definitions for adding content of tasks

#### static/
styles.css  ->  contains CSS stylings
tasks.js    ->  JS logic for accordions, collapsing tasks and interactivity of nested depedencies
add_task.js ->  JS logic to add task form

### templates/
layout.html -> contants imports, and references while adding navbar for use that is inherited by subsequent htmls
index.html  -> display the main task view
task_detail -> shows details of any of the selected asks, ability to add dependencies or delete itself and all other subtasks within
task_item   -> renders tasks within the accordions.

login.html  -> for authentication via login
register    -> allows for creation of accounts

## How to Run

Firstly use the commands:

(Note: I use python3)

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver to activate server

Register an account or log in if you already have one.

After logging in, you can add tasks using the Add Task which is the floating + button. Each task can have a title, description, and can be marked as completed or in progress.

## Future Improvements

Possible changes for the future include:

- Converting to a mobile app or deployment as a real web app
- Fixing accordion indents
- Adding time related features namely deadlines
- Categories that include customizable ones or prebuilt ones