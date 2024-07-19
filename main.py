from customtkinter import *
from PIL import Image, ImageTk
from tkinter import Label, StringVar, IntVar, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pygame
import sqlite3
import database

set_default_color_theme("NightTrain.json")

database.initialize_db()

# Sign-up window
def signup_window():
    signup_win = CTkToplevel()
    signup_win.geometry("300x500")
    signup_win.resizable(0, 0)

    signup_label = CTkLabel(master=signup_win, text="Sign Up", font=("Arial", 20))
    signup_label.pack(pady=10)

    username_label = CTkLabel(master=signup_win, text="Username:", font=("Arial", 14))
    username_label.pack(pady=5)
    username_entry = CTkEntry(master=signup_win)
    username_entry.pack(pady=5)

    password_label = CTkLabel(master=signup_win, text="Password:", font=("Arial", 14))
    password_label.pack(pady=5)
    password_entry = CTkEntry(master=signup_win, show="*")
    password_entry.pack(pady=5)

    confirm_password_label = CTkLabel(master=signup_win, text="Confirm Password:", font=("Arial", 14))
    confirm_password_label.pack(pady=5)
    confirm_password_entry = CTkEntry(master=signup_win, show="*")
    confirm_password_entry.pack(pady=5)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        elif username and password:
            try:
                database.add_user(username, password)
                messagebox.showinfo("Success", "User registered successfully")
                signup_win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    signup_button = CTkButton(master=signup_win, text="Sign Up", command=register_user)
    signup_button.pack(pady=20)

    signup_win.mainloop()


# Login window
def login_window():
    login_win = CTk()
    login_win.geometry("300x400")
    login_win.resizable(0, 0)

    login_label = CTkLabel(master=login_win, text="Login", font=("Arial", 20))
    login_label.pack(pady=10)

    username_label = CTkLabel(master=login_win, text="Username:", font=("Arial", 14))
    username_label.pack(pady=5)
    username_entry = CTkEntry(master=login_win)
    username_entry.pack(pady=5)

    password_label = CTkLabel(master=login_win, text="Password:", font=("Arial", 14))
    password_label.pack(pady=5)
    password_entry = CTkEntry(master=login_win, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if database.check_credentials(username, password):
            login_win.destroy()
            main_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_button = CTkButton(master=login_win, text="Login", command=attempt_login)
    login_button.pack(pady=20)

    signup_button = CTkButton(master=login_win, text="Sign Up", command=signup_window)
    signup_button.pack(pady=20)

    login_win.mainloop()

task_list = []
previous_tasks_done = 0
tasks = []
checkboxes = []

def main_window(username):
    global task_list
    user_id = database.get_user_id(username)
    task_list = database.get_tasks_from_db(user_id)

    app = CTk()
    app.geometry("900x650")
    app.resizable(0, 0)
    set_appearance_mode("dark")

    # Sol siyah çerçeve
    left_frame = CTkFrame(master=app, fg_color="black", width=216, height=650, corner_radius=0)
    left_frame.pack_propagate(0)
    left_frame.pack(fill="y", anchor="w", side="left")

    # logo ikonu
    logo_img_data = Image.open("resim_2024-07-17_170423158.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(90, 100))

    CTkLabel(master=left_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    # analitik butonu
    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    CTkButton(master=left_frame, image=analytics_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(60, 0))

    # ... butonu
    package_img_data = Image.open("package_icon.png")
    package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)

    CTkButton(master=left_frame, image=package_img, text="Orders", fg_color="transparent", font=("Arial Bold", 14),
              text_color="white",
              hover_color="#eee", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

    # ...2 butonu
    list_img_data = Image.open("list_icon.png")
    list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
    CTkButton(master=left_frame, image=list_img, text="Orders", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

    # ...3 butonu
    returns_img_data = Image.open("calendar_icon.png")
    returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    CTkButton(master=left_frame, image=returns_img, text="Calendar", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w", command=lambda: open_calendar_window()).pack(anchor="center", ipady=5,
                                                                                              pady=(16, 0))

    # hesap butonu
    person_img_data = Image.open("person_icon.png")
    person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
    CTkButton(master=left_frame, image=person_img, text="Account", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(160, 0))

    # ayarlar butonu
    settings_img_data = Image.open("settings.png")
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
    CTkButton(master=left_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

    # sağ arkaplan
    right_bg_image_data = Image.open("tp238-background-03 (1) (2).jpg")
    right_bg_image = CTkImage(dark_image=right_bg_image_data, light_image=right_bg_image_data, size=(685, 650))

    right_frame = CTkFrame(master=app, fg_color="transparent", width=685, height=650, corner_radius=0)
    right_frame.pack_propagate(0)
    right_frame.place(x=215, y=0)

    CTkLabel(master=right_frame, text="", image=right_bg_image).place(x=0, y=0)

    # üst_frame
    top_frame = CTkFrame(master=app, fg_color="black", bg_color="black", width=300, height=100, corner_radius=0)
    top_frame.pack_propagate(0)
    top_frame.place(x=280, y=30)

    # üst frame title
    title = CTkLabel(master=top_frame, text="Welcome Back!\n Semih ", text_color="white",
                     font=("Century Gothic", 35, "bold"))
    title.place(x=10, y=10)

    # Görev ekle butonu
    add_img = Image.open("add-circle-svgrepo-com (1).png").convert("RGBA")
    add_img = add_img.resize((40, 40))
    add_ctk_image = CTkImage(dark_image=add_img, light_image=add_img)

    add_button = CTkButton(master=app, text="Add Task", corner_radius=12, command=lambda: add_task_window(),
                           image=add_ctk_image)
    add_button.place(x=360, y=220)

    # Görev silme butonu
    remove_img = Image.open("trash-svgrepo-com (1).png").convert("RGBA")
    remove_img = remove_img.resize((40, 40))
    remove_ctk_image = CTkImage(dark_image=remove_img, light_image=remove_img)

    remove_button = CTkButton(master=app, text="Remove Task", corner_radius=12, command=lambda: remove_task_window(),
                              image=remove_ctk_image)
    remove_button.place(x=360, y=270)

    # Görev çerçevesi
    checkbox_frame = CTkScrollableFrame(master=app, border_color="MediumPurple3", border_width=2, width=200, height=350,
                                        corner_radius=5)
    checkbox_frame.place(x=600, y=200)

    # Yapılan iş kalan iş çerçevesi
    task_status_frame = CTkFrame(master=app, border_color="MediumPurple3", border_width=1, width=300, height=100,
                                 corner_radius=4)
    task_status_frame.place(x=280, y=340)

    # Tik işareti ikonu
    tik_image_data = Image.open("checked-svgrepo-com.png")
    tik_image = CTkImage(dark_image=tik_image_data, light_image=tik_image_data, size=(45, 45))
    CTkLabel(master=task_status_frame, image=tik_image, text="").place(x=10, y=26)

    # Task status yazısı
    task_status_label = CTkLabel(master=task_status_frame, text="Task Status", font=("Arial Black", 18))
    task_status_label.place(x=70, y=10)

    tasks_done_label = CTkLabel(master=task_status_frame, text="Tasks Done: 0", font=("Arial", 12))
    tasks_done_label.place(x=70, y=35)

    tasks_remaining_label = CTkLabel(master=task_status_frame, text="Tasks Remaining: 0", font=("Arial", 12))
    tasks_remaining_label.place(x=70, y=60)

    # Success frame
    success_frame = CTkFrame(master=app, border_color="DeepSkyBlue2", border_width=1, width=300, height=100,
                             corner_radius=4)
    success_frame.place(x=280, y=460)

    # Success ikonu
    success_image_data = Image.open("success.png")
    success_image = CTkImage(dark_image=success_image_data, light_image=success_image_data, size=(55, 55))
    CTkLabel(master=success_frame, image=success_image, text="").place(x=10, y=26)

    # Success label
    success_percentage_label = CTkLabel(master=success_frame, text="Success Percentage", font=("Arial Black", 18))
    success_percentage_label.place(x=70, y=10)
    # Success percentage value label
    success_percentage_value_label = CTkLabel(master=success_frame, text="0%", font=("Arial", 30))
    success_percentage_value_label.place(x=142, y=50)


    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\semih\PycharmProjects\TO-DO LIST APP\success_bell-6776.mp3")


    user_id = database.get_user_id(username)
    tasks = database.get_tasks_from_db(user_id)
    # Kullanıcının görevlerini burada yükleyip ekranda gösterebilirsiniz
    for task_id, task_text, task_status in tasks:
        var = IntVar(value=task_status)
        checkbox = CTkCheckBox(master=checkbox_frame, text=task_text, variable=var, command=lambda: database.update_task_status_in_db(task_id, var.get()))
        checkbox.pack(anchor="w", padx=10, pady=5)
        task_list.append((task_id, var))

    def update_task_status():
        global previous_tasks_done
        tasks_done = sum(1 for task_id, var in checkboxes if var.get() == 1)
        tasks_remaining = len(task_list) - tasks_done
        tasks_done_label.configure(text=f"Tasks Done: {tasks_done}")
        tasks_remaining_label.configure(text=f"Tasks Remaining: {tasks_remaining}")

        if len(task_list) > 0:
            success_percentage = int((tasks_done / len(task_list)) * 100)
        else:
            success_percentage = 0
        success_percentage_value_label.configure(text=f"{success_percentage}%")

        if tasks_done > previous_tasks_done:
            pygame.mixer.music.play()

        previous_tasks_done = tasks_done

        for task_id, var in checkboxes:
            database.update_task_status_in_db(task_id, var.get())

    def open_calendar_window():
        calendar_window = CTkToplevel(app)
        calendar_window.geometry("300x300")
        calendar_window.resizable(0, 0)

        new_calendar_x = app.winfo_x() + (app.winfo_width() - 300) // 2
        new_calendar_y = app.winfo_y() + (app.winfo_height() - 300) // 2

        calendar_window.geometry(f"300x300+{new_calendar_x}+{new_calendar_y}")
        calendar_window.transient(app)
        calendar_window.grab_set()

        today = datetime.today()
        cal = Calendar(calendar_window, selectmode='day', year=today.year, month=today.month, day=today.day)
        cal.pack(pady=90)

        def select_date():
            selected_date = cal.selection_get()
            # Burada seçilen tarihi kullanabilirsiniz
            print(f"Seçilen tarih: {selected_date}")
            calendar_window.destroy()

        CTkButton(master=calendar_window, text="Select Date", command=select_date).pack(pady=10)

    def add_task(task):
        var = IntVar()
        checkbox = CTkCheckBox(master=checkbox_frame, text=task, variable=var, command=update_task_status)
        checkbox.pack(anchor="w", padx=10, pady=5)
        tasks.append(task)
        checkboxes.append(var)
        update_task_status()

    def add_task_window():
        new_task_window = CTkToplevel(app)
        new_task_window.geometry("300x250")
        new_task_window.resizable(0, 0)

        app_x = app.winfo_x()
        app_y = app.winfo_y()
        app_width = app.winfo_width()
        app_height = app.winfo_height()

        new_window_width = 300
        new_window_height = 250

        new_x = app_x + (app_width - new_window_width) // 2
        new_y = app_y + (app_height - new_window_height) // 2

        new_task_window.geometry(f"{new_window_width}x{new_window_height}+{new_x}+{new_y}")
        new_task_window.transient(app)
        new_task_window.grab_set()

        task_label = CTkLabel(master=new_task_window, text="Task Name:", font=("Arial", 14))
        task_label.pack(pady=10)

        task_entry = CTkEntry(master=new_task_window, placeholder_text="Enter a task...", width=250)
        task_entry.pack(pady=5)

        def open_calendar():
            calendar_window = CTkToplevel(app)
            calendar_window.geometry("300x300")
            calendar_window.resizable(0, 0)

            calendar_window.geometry(f"{300}x{300}+{new_x}+{new_y}")
            calendar_window.transient(app)
            calendar_window.grab_set()

            today = datetime.today()
            cal = Calendar(calendar_window, selectmode='day', year=today.year, month=today.month, day=today.day,
                           date_pattern='dd.mm.yyyy')
            cal.pack(pady=20)

            def select_date():
                selected_date = cal.selection_get()
                selected_due_date.set(selected_date.strftime("%d.%m.%Y"))
                calendar_window.destroy()

            select_button = CTkButton(master=calendar_window, text="Select Date", command=select_date)
            select_button.pack(pady=10)

        selected_due_date = StringVar()
        selected_due_date.set("No date selected")

        def save_task():
            task_name = task_entry.get()
            if task_name:
                database.add_task_to_db(user_id, task_name)
                new_task_window.destroy()
                refresh_task_list()

        save_button = CTkButton(master=new_task_window, text="Save Task", command=save_task)
        save_button.pack(pady=20)

        date_options = ["No Due Date", "Today", "Tomorrow", "Next Week", "Pick a Date"]
        selected_date_option = StringVar(value=date_options[0])

        def handle_date_option(choice):
            if choice == "Today":
                selected_due_date.set(datetime.today().strftime("%d.%m.%Y"))
            elif choice == "Tomorrow":
                selected_due_date.set((datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y"))
            elif choice == "Next Week":
                selected_due_date.set((datetime.today() + timedelta(weeks=1)).strftime("%d.%m.%Y"))
            elif choice == "Pick a Date":
                open_calendar()

        date_menu = CTkOptionMenu(new_task_window, values=date_options, command=handle_date_option,
                                  variable=selected_date_option)
        date_menu.pack(pady=10)

        selected_date_label = CTkLabel(master=new_task_window, textvariable=selected_due_date)
        selected_date_label.pack(pady=5)

        save_button = CTkButton(master=new_task_window, text="Save Task", command=save_task)
        save_button.pack(pady=20)

    def refresh_task_list():
        # Mevcut checkbox'ları temizle
        for widget in checkbox_frame.winfo_children():
            widget.destroy()

        # Görev listesini ve checkbox'ları yeniden doldur
        global task_list
        task_list = database.get_tasks_from_db(user_id)
        checkboxes.clear()  # Önceki checkbox'ları temizle

        for task_id, task_text, task_status in task_list:
            var = IntVar(value=task_status)
            checkbox = CTkCheckBox(master=checkbox_frame, text=task_text, variable=var, command=update_task_status)
            checkbox.pack(anchor="w", padx=10, pady=5)
            checkboxes.append((task_id, var))

    def remove_task_window():
        remove_window = CTkToplevel(app)
        remove_window.geometry("300x350")
        remove_window.resizable(0, 0)

        new_x = app.winfo_x() + (app.winfo_width() - 300) // 2
        new_y = app.winfo_y() + (app.winfo_height() - 350) // 2

        remove_window.geometry(f"300x350+{new_x}+{new_y}")
        remove_window.transient(app)
        remove_window.grab_set()

        remove_label = CTkLabel(master=remove_window, text="Select tasks to remove:", font=("Arial", 14))
        remove_label.pack(pady=10)

        remove_frame = CTkScrollableFrame(master=remove_window, width=250, height=200)
        remove_frame.pack(pady=10)

        remove_vars = []
        for task, checkbox in zip(tasks, checkboxes):
            var = IntVar()
            remove_checkbox = CTkCheckBox(master=remove_frame, text=task, variable=var)
            remove_checkbox.pack(anchor="w", padx=10, pady=5)
            remove_vars.append((task, var))

        def remove_selected_tasks():
            global tasks, checkboxes
            new_tasks = []
            new_checkboxes = []

            task_ids_to_remove = [task_id for (task_id, _), (remove_task, remove_var) in zip(checkboxes, remove_vars) if
                                  remove_var.get() == 1]

            # Veritabanından görevleri sil
            for task_id in task_ids_to_remove:
                database.remove_task_from_db(task_id)

            # Görev listesini güncelle
            for (task_id, checkbox_loop), (remove_task, remove_var) in zip(checkboxes, remove_vars):
                if remove_var.get() == 0:
                    new_tasks.append(task_id)
                    new_checkboxes.append(checkbox_loop)

            tasks = new_tasks
            checkboxes = new_checkboxes
            update_task_status()
            remove_window.destroy()
            refresh_task_list()

        CTkButton(master=remove_window, text="Remove Selected Tasks", command=remove_selected_tasks).pack(pady=10)

    refresh_task_list()
    update_task_status()

    app.mainloop()



login_window()
