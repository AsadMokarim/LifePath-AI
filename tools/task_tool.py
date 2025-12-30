import json
import os

TASK_FILE = "data/tasks.json"


def load_tasks():
    """
    Load all tasks from the JSON file.
    Returns a list.
    """
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    """
    Save all tasks to the JSON file.
    """
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(title, estimated_time="unknown", priority="medium"):
    """
    Add a new task to memory.
    """
    tasks = load_tasks()

    task = {
        "title": title,
        "estimated_time": estimated_time,
        "priority": priority,
        "status": "todo"
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def get_tasks():
    """
    Return all tasks.
    """
    return load_tasks()


