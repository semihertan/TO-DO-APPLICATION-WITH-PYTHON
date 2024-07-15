import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Task:
    def __init__(self, title, description=''):
        self.title = title
        self.description = description
        self.completed = False

    def __str__(self):
        status = "COMPLETED" if self.completed else "NOT COMPLETED"
        return f"{self.title}: {status}"

class ToDoApp:
    def __init__(self, root, user_name):
        self.root = root
        self.root.title(f"ToDo App - Welcome, {user_name}!")
        self.tasks = []
        self.root.geometry("1000x650")

        # En üst frame
        self.top_frame = tk.Frame(self.root, bg="red", height=50)
        self.top_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        self.title_label_top = tk.Label(self.top_frame, text=f"Welcome to ToDo App, {user_name}!", bg="red", fg="white",
                                        font=("Arial", 20), anchor="w")
        self.title_label_top.pack(side=tk.LEFT, padx=10, pady=10)

        today_date = datetime.now().strftime("%d.%m.%Y")
        self.date_label = tk.Label(self.top_frame, text=today_date, bg="red", fg="white", font=("Arial", 20),
                                   anchor="e")
        self.date_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.time_label = tk.Label(self.top_frame, bg="red", fg="white", font=("Arial", 20), anchor="e")
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update_time()

        # Alt main frame
        self.bottom_frame = tk.Frame(self.root, bg="black")
        self.bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Sol üst taraf
        self.title_label = tk.Label(self.bottom_frame, text="TO-DO TITLE: ")
        self.title_label.pack()

        self.title_entry = tk.Entry(self.bottom_frame)
        self.title_entry.pack()

        self.description_label = tk.Label(self.bottom_frame, text="DESCRIPTION: ")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.bottom_frame)
        self.description_entry.pack()

        self.add_button = tk.Button(self.bottom_frame, text="ADD TASK", padx=10, pady=10, command=self.add_task)
        self.add_button.pack()

        # Sağ frame
        self.right_frame = tk.Frame(self.bottom_frame, bg="blue")
        self.right_frame.pack(side=tk.RIGHT, padx=80, pady=10)

        self.task_listbox = tk.Listbox(self.right_frame, height=15, width=80, bg="white", font=("Arial", 14))
        self.task_listbox.pack()

        self.complete_button = tk.Button(self.right_frame, text="COMPLETE", command=self.complete_task)
        self.complete_button.pack()

        # Görev detayları
        self.details_label = tk.Label(self.right_frame, text="Task Details", bg="blue", fg="white", font=("Arial", 15))
        self.details_label.pack(pady=10)

        self.description_label = tk.Label(self.right_frame, text="", bg="blue", fg="white", font=("Arial", 12))
        self.description_label.pack(pady=10)

        self.task_listbox.bind('<<ListboxSelect>>', self.show_task_details)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

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
            status = "COMPLETED" if task.completed else "NOT COMPLETED"
            color = "green" if task.completed else "red"
            self.task_listbox.insert(tk.END, f"{task.title}: {status}")
            self.task_listbox.itemconfig(tk.END, {'fg': color})

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index].completed = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task")

    def show_task_details(self, event):
        try:
            index = self.task_listbox.curselection()[0]
            selected_task = self.tasks[index]
            self.description_label.config(text=selected_task.description)
        except IndexError:
            self.description_label.config(text="")

if __name__ == "__main__":
    # Kullanıcıdan ad ve soyad almak için küçük pencereyi oluşturmadan önce
    temp_root = tk.Tk()
    temp_root.withdraw()

    user_name = simpledialog.askstring("Input", "Please enter your name and surname:", parent=temp_root)
    if not user_name:
        user_name = "User"

    temp_root.destroy()

    root = tk.Tk()
    app = ToDoApp(root, user_name)
    root.mainloop()
