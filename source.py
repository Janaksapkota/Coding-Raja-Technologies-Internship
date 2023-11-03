import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

# Task data structure
class Task:
    def __init__(self, title, priority, due_date):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False

# Command-line functions
def add_task_cli(tasks, title, priority, due_date):
    new_task = Task(title, priority, due_date)
    tasks.append(new_task)

def remove_task_cli(tasks, index):
    if 0 <= index < len(tasks):
        del tasks[index]
    else:
        print("Invalid task index.")

def complete_task_cli(tasks, index):
    if 0 <= index < len(tasks):
        tasks[index].completed = True
    else:
        print("Invalid task index.")

def display_tasks_cli(tasks):
    for index, task in enumerate(tasks):
        status = "Completed" if task.completed else "Not Completed"
        print(f"{index + 1}. {task.title} (Priority: {task.priority}, Due Date: {task.due_date}, Status: {status})")

def save_tasks_to_file(filename, tasks):
    with open(filename, 'w') as file:
        task_list = [{'title': task.title, 'priority': task.priority, 'due_date': task.due_date, 'completed': task.completed}
                     for task in tasks]
        json.dump(task_list, file)

def load_tasks_from_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        task_list = json.load(file)
        tasks = [Task(task['title'], task['priority'], task['due_date']) for task in task_list]
        for i, task in enumerate(tasks):
            task.completed = task_list[i]['completed']
        return tasks

# Tkinter functions
def add_task_gui():
    task = entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()
    if task:
        add_task_cli(tasks, task, priority, due_date)
        save_tasks_to_file(filename, tasks)
        entry.delete(0, tk.END)
        refresh_task_list()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def remove_task_gui():
    try:
        selected_task_index = task_listbox.curselection()[0]
        index = int(selected_task_index)
        remove_task_cli(tasks, index)
        save_tasks_to_file(filename, tasks)
        refresh_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def complete_task_gui():
    try:
        selected_task_index = task_listbox.curselection()[0]
        index = int(selected_task_index)
        complete_task_cli(tasks, index)
        save_tasks_to_file(filename, tasks)
        refresh_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

def refresh_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task.completed else "Not Completed"
        task_listbox.insert(tk.END, f"{task.title} (Priority: {task.priority}, Due Date: {task.due_date}, Status: {status})")

# Load tasks from file
filename = "tasks.json"
tasks = load_tasks_from_file(filename)

# Tkinter setup
root = tk.Tk()
root.title("To-Do List")

entry = tk.Entry(root, width=40)
add_button = tk.Button(root, text="Add Task", command=add_task_gui)
remove_button = tk.Button(root, text="Remove Task", command=remove_task_gui)
complete_button = tk.Button(root, text="Mark Completed", command=complete_task_gui)

priority_var = tk.StringVar(root)
priority_var.set("Medium")
priority_label = tk.Label(root, text="Priority:")
priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")

due_date_label = tk.Label(root, text="Due Date:")
due_date_entry = tk.Entry(root, width=40)

task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40)
refresh_task_list()

entry.pack(pady=10)
add_button.pack()
remove_button.pack()
complete_button.pack()
priority_label.pack()
priority_menu.pack()
due_date_label.pack()
due_date_entry.pack()
task_listbox.pack()

root.mainloop()
