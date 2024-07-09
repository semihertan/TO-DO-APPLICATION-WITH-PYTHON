import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, title, description=''):
        self.title = title
        self.description = description
        self.completed = False

    def __str__(self):
        if self.completed:
            status = "COMPLETED"
        else:
            status = "NOT COMPLETED"
        return f"{self.title}: {status}"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo App")
        self.tasks = []

        # Sol frame
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.title_label = tk.Label(self.left_frame, text="TO-DO TITLE: ")
        self.title_label.pack()

        self.title_entry = tk.Entry(self.left_frame)
        self.title_entry.pack()

        self.description_label = tk.Label(self.left_frame, text="DESCRIPTION: ")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.left_frame)
        self.description_entry.pack()

        self.add_button = tk.Button(self.left_frame, text="ADD TASK", command=self.add_task)
        self.add_button.pack()

        # Sağ frame
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.right_frame, height=15, width=40)
        self.task_listbox.pack()

        self.complete_button = tk.Button(self.right_frame, text="COMPLETE", command=self.complete_task)
        self.complete_button.pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()

        if title:
            new_task = Task(title, description)
            self.tasks.append(new_task)
            self.update_task_listbox()
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a title")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index].completed = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
