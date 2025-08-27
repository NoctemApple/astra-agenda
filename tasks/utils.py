def build_task_tree(tasks):
    task_dict = {task.id: {"task": task, "children": []} for task in tasks}

    for task in tasks:
        for dep in task.dependencies.all():
            task_dict[dep.id]["children"].append(task_dict[task.id])

    # return only roots (tasks with no dependencies)
    roots = [v for v in task_dict.values() if not v["task"].dependencies.exists()]
    return roots
