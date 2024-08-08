from customtkinter import *
from PIL import Image
from tkinter import StringVar, IntVar, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import threading
import pygame
import sqlite3
import database
from plyer import notification
import time

set_default_color_theme("NightTrain.json")

database.initialize_db()

signup_bg_data = Image.open("signup_bg.jpg")
login_bg_data = Image.open("login_bg_3.jpg")
username_icon_data = Image.open("username_icon.png")
password_icon_data = Image.open("password_icon.png")
google_icon_data = Image.open("google-icon.png")

signup_bg_image = CTkImage(dark_image=signup_bg_data, light_image=signup_bg_data, size=(300, 500))
login_bg_image = CTkImage(dark_image=login_bg_data, light_image=login_bg_data, size=(300, 480))
username_icon = CTkImage(dark_image=username_icon_data, light_image=username_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

# Sign-up window
def signup_window():
    signup_win = CTkToplevel()
    signup_win.title("Sign Up")
    signup_win.geometry("300x450")
    signup_win.resizable(0, 0)

    CTkLabel(master=signup_win, text="Welcome among us!", text_color="SkyBlue4", anchor="w", justify="left",
             font=("Arial", 24, "bold")).pack(anchor="w", pady=(50, 5), padx=(37, 0))
    CTkLabel(master=signup_win, text="Enter a username and password to register", text_color="salmon3", anchor="w", justify="left",
             font=("Arial", 10, "bold")).pack(anchor="w", padx=(37, 0))

    CTkLabel(master=signup_win, text="  Username", text_color="SkyBlue4", anchor="w", justify="left", font=("Arial", 14, "bold"),
             image=username_icon, compound="left").pack(anchor="w", pady=(30, 0), padx=(37, 0))
    username_entry = CTkEntry(master=signup_win, width=225, fg_color="#EEEEEE", border_color="SkyBlue4", border_width=2, text_color="#000000")
    username_entry.pack(anchor="w", padx=(37, 0))

    # password label and entry
    CTkLabel(master=signup_win, text="  Password", text_color="SkyBlue4", anchor="w", justify="left",
             font=("Arial", 14, "bold"), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0),padx=(37, 0))
    password_entry = CTkEntry(master=signup_win, width=225, fg_color="#EEEEEE", border_color="SkyBlue4", border_width=2,
                              text_color="#000000")
    password_entry.pack(anchor="w", padx=(37, 0))

    CTkLabel(master=signup_win, text="  Confirm Password", text_color="SkyBlue4", anchor="w", justify="left",
             font=("Arial", 14, "bold"), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(37, 0))
    confirm_password_entry = CTkEntry(master=signup_win, width=225, fg_color="#EEEEEE", border_color="SkyBlue4", border_width=2,
                              text_color="#000000")
    confirm_password_entry.pack(anchor="w", padx=(37, 0))

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

    signup_button = CTkButton(master=signup_win, text="Sign Up", fg_color="SkyBlue4", hover_color="SteelBlue4",
                              font=("Arial", 12, "bold"), text_color="#ffffff", width=225, command=register_user).pack(anchor="w",
                              pady=(20, 0), padx=(37, 0))

    signup_win.mainloop()

# Login window
def login_window():
    login_win = CTk()
    login_win.title("Login")
    login_win.geometry("600x480")
    login_win.resizable(0, 0)

    CTkLabel(master=login_win, text="", image=login_bg_image).pack(expand=True, side="left")

    # login right frame
    frame = CTkFrame(master=login_win, width=300, height=480, fg_color="lavender", bg_color="mint cream", corner_radius=0)
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Welcome Back!", text_color="SkyBlue4", anchor="w", justify="left",
             font=("Arial", 24, "bold")).pack(anchor="w", pady=(50, 5), padx=(37, 0))
    CTkLabel(master=frame, text="Sign in to your account", text_color="salmon3", anchor="w", justify="left",
             font=("Arial", 12, "bold")).pack(anchor="w", padx=(37, 0))

    # username label and entry
    CTkLabel(master=frame, text="  Username", text_color="SkyBlue4", anchor="w", justify="left", font=("Arial", 14, "bold"),
             image=username_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(37, 0))
    username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="SkyBlue4", border_width=2,
             text_color="#000000")
    username_entry.pack(anchor="w", padx=(37, 0))

    # password label and entry
    CTkLabel(master=frame, text="  Password", text_color="SkyBlue4", anchor="w", justify="left",
             font=("Arial", 14, "bold"), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(37, 0))
    password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="SkyBlue4", border_width=2, text_color="#000000",
             show="*")
    password_entry.pack(anchor="w", padx=(37, 0))

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if database.check_credentials(username, password):
            login_win.destroy()
            main_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    CTkButton(master=frame, text="Log in", fg_color="SkyBlue4", hover_color="SteelBlue4", font=("Arial", 12, "bold"),
              text_color="#ffffff", width=225, command=attempt_login).pack(anchor="w", pady=(40, 0), padx=(37, 0))

    CTkLabel(master=frame, text="Don't have an account?", text_color="salmon3", anchor="w", justify="left",
             font=("Arial", 12, "bold")).pack(anchor="w",pady=(30, 0), padx=(37, 0))

    signup_button = CTkButton(master=frame, text="Sign Up", fg_color="SkyBlue4", hover_color="SteelBlue4", font=("Arial", 12, "bold"),
              text_color="#ffffff", width=225, command=signup_window).pack(anchor="w", pady=(10, 0), padx=(37, 0))

    login_win.mainloop()

task_list = []
previous_tasks_done = 0
tasks = []
checkboxes = []

def main_window(username):
    global task_list
    user_id = database.get_user_id(username)
    task_list = database.get_tasks_from_db(user_id)
    past_due_tasks = database.get_past_due_tasks(user_id)
    database.remove_past_due_tasks(user_id)


    app = CTk()
    app.title("ERTAN")
    app.geometry("1000x650")
    app.resizable(0, 0)
    set_appearance_mode("dark")

    # Sol siyah çerçeve
    left_frame = CTkFrame(master=app, fg_color="black", width=216, height=650, corner_radius=0)
    left_frame.pack_propagate(0)
    left_frame.pack(fill="y", anchor="w", side="left")

    # logo ikonu
    logo_img_data = Image.open("logo.jpeg")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(165, 155))

    CTkLabel(master=left_frame, text="", image=logo_img).pack(pady=(0, 0), anchor="center")

    CTkLabel(master=left_frame, text=f"Welcome Back\n{username}", font=("LeagueSpartan", 12, "bold")).pack(pady=(5, 0))

    # hesap butonu
    person_img_data = Image.open("person_icon.png")
    person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
    CTkButton(master=left_frame, image=person_img, text="Account", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w").pack(anchor="center", ipady=5, pady=(100, 0))

    # notifications button
    notification_number_var = StringVar()
    notification_number_var.set(f"{len(past_due_tasks)}")
    list_img_data = Image.open("list_icon.png")
    list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
    CTkButton(master=left_frame, image=list_img, text="Notifications", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w", command=lambda: notifications_window()).pack(anchor="center", ipady=5, pady=(16, 0))

    notification_number_label = CTkLabel(master=left_frame, textvariable=notification_number_var, fg_color="black", font=("Arial", 14))
    notification_number_label.place(x=25, y=255)

    # calendar button
    returns_img_data = Image.open("calendar_icon.png")
    returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    CTkButton(master=left_frame, image=returns_img, text="Calendar", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w", command=lambda: open_calendar_window()).pack(anchor="center", ipady=5,
                                                                                              pady=(16, 0))


    # ayarlar butonu
    settings_img_data = Image.open("settings.png")
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
    CTkButton(master=left_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14),
              hover_color="#121424", anchor="w", command=lambda: settings_window()).pack(anchor="center", ipady=5, pady=(159, 0))

    # sağ arkaplan
    right_bg_image_data = Image.open("and Sparkle! (1).png")
    right_bg_image = CTkImage(dark_image=right_bg_image_data, light_image=right_bg_image_data, size=(785, 650))

    right_frame = CTkFrame(master=app, fg_color="transparent", width=785, height=650, corner_radius=0)
    right_frame.pack_propagate(0)
    right_frame.place(x=215, y=0)

    CTkLabel(master=right_frame, text="", image=right_bg_image).place(x=0, y=0)



    # buttons main frame
    buttons_frame = CTkFrame(master=app, corner_radius=0, fg_color="black", bg_color="black", width=260, height=50)
    buttons_frame.place(x=720, y=305)

    # Görev ekle butonu
    add_img = Image.open("add_icon.png").convert("RGBA")
    add_img = add_img.resize((40, 40))
    add_ctk_image = CTkImage(dark_image=add_img, light_image=add_img)

    add_button = CTkButton(master=buttons_frame, text="", corner_radius=10, width=10, height=30, command=lambda: add_task_window(),
                           image=add_ctk_image)
    add_button.place(x=0, y=10)

    # Görev silme butonu
    remove_img = Image.open("trash-svgrepo-com (1).png").convert("RGBA")
    remove_img = remove_img.resize((40, 40))
    remove_ctk_image = CTkImage(dark_image=remove_img, light_image=remove_img)

    remove_button = CTkButton(master=buttons_frame, text="", corner_radius=10, width=10, height=30, command=lambda: remove_task_window(),
                              image=remove_ctk_image)
    remove_button.place(x=50, y=10)

    # sorting filter option menu
    sort_menu = CTkOptionMenu(master=buttons_frame, width=150, height=31,
                              values=["Sort by Favorite", "Sort by Due Date", "Sort Alphabetically"],
                              command=lambda criteria: refresh_task_list(criteria))
    sort_menu.place(x=100, y=10)

    # Görev çerçevesi
    checkbox_frame = CTkScrollableFrame(master=app, fg_color="black", bg_color="black", width=480, height=245,
                                        corner_radius=5)
    checkbox_frame.place(x=470, y=350)

    # Yapılan iş kalan iş çerçevesi
    task_status_frame = CTkFrame(master=app, fg_color="black", border_color="MediumPurple3", border_width=1, width=200, height=100,
                                 corner_radius=5)
    task_status_frame.place(x=230, y=350)

    # Tik işareti ikonu
    tik_image_data = Image.open("status_icon.png")
    tik_image = CTkImage(dark_image=tik_image_data, light_image=tik_image_data, size=(45, 45))
    CTkLabel(master=task_status_frame, image=tik_image, text="").place(x=10, y=26)

    # Task status yazısı
    task_status_label = CTkLabel(master=task_status_frame, text="Task Status", font=("Arial", 15, "bold"))
    task_status_label.place(x=70, y=10)

    tasks_done_label = CTkLabel(master=task_status_frame, text="Tasks Done: 0", font=("Arial", 11))
    tasks_done_label.place(x=70, y=35)

    tasks_remaining_label = CTkLabel(master=task_status_frame, text="Tasks Remaining: 0", font=("Arial", 11))
    tasks_remaining_label.place(x=70, y=60)

    # Success frame
    success_frame = CTkFrame(master=app, fg_color="black", border_color="MediumPurple3", border_width=1, width=200, height=100,
                             corner_radius=5)
    success_frame.place(x=230, y=480)

    # Success ikonu
    success_image_data = Image.open("success.png")
    success_image = CTkImage(dark_image=success_image_data, light_image=success_image_data, size=(55, 55))
    CTkLabel(master=success_frame, image=success_image, text="").place(x=15, y=22)

    # Success percentage value label
    success_percentage_value_label = CTkLabel(master=success_frame, text="0%", font=("Arial", 30))
    success_percentage_value_label.place(x=107, y=33)

    CTkLabel(master=app, text="developed by SEMIH ERTAN", text_color="gray25", fg_color="black", font=("LeagueSpartan", 6, "bold")).place(x=911, y=630)


    # sound effect loading
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\semih\PycharmProjects\TO-DO LIST APP\success_bell-6776.mp3")



    tasks = database.get_tasks_from_db(user_id)
    # getting user id and user tasks from db
    for task_id, task_text, task_status, is_favorite, due_date, repeat_interval, reminder_time in tasks:
        var = IntVar(value=task_status)
        checkbox = CTkCheckBox(master=checkbox_frame, text=task_text, variable=var, command=lambda: database.update_task_status_in_db(task_id, var.get()))
        checkbox.pack(anchor="w", padx=10, pady=5)
        task_list.append((task_id, var))


    def update_task_status():
        global previous_tasks_done
        tasks_done = sum(1 for task_id, var in checkboxes if var.get() == 1)
        tasks_remaining = len(checkboxes) - tasks_done
        tasks_done_label.configure(text=f"Tasks Done: {tasks_done}")
        tasks_remaining_label.configure(text=f"Tasks Remaining: {tasks_remaining}")

        if len(checkboxes) > 0:
            success_percentage = int((tasks_done / len(checkboxes)) * 100)
        else:
            success_percentage = 0
        success_percentage_value_label.configure(text=f"%{success_percentage}")

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


    def notifications_window():
        notifications_window = CTkToplevel(app)
        notifications_window.geometry("500x500")
        notifications_window.title("Notifications")
        notifications_window.resizable(0, 0)

        new_window_x = app.winfo_x() + (app.winfo_width() - 500) // 2
        new_window_y = app.winfo_y() + (app.winfo_height() - 500) // 2

        notifications_window.geometry(f"500x500+{new_window_x}+{new_window_y}")
        notifications_window.transient(app)
        notifications_window.grab_set()

        past_tasks_label = CTkLabel(master=notifications_window, text="You have overdue tasks", font=("Arial", 30, "bold"))
        past_tasks_label.pack(padx=25, pady=20, anchor="w")

        past_tasks_frame = CTkScrollableFrame(master=notifications_window, width=300, height=200)
        past_tasks_frame.pack(pady=10)

        for task in past_due_tasks:
            task_name, due_date = task
            task_label = CTkLabel(master=past_tasks_frame, text=f"{task_name}   {due_date}", text_color="red")
            task_label.pack(padx=5, pady=5, anchor="w")

    def settings_window():
        settings_window = CTkToplevel(app)
        settings_window.geometry("500x500")
        settings_window.title("Settings")
        settings_window.resizable(0, 0)

        new_x = app.winfo_x() + (app.winfo_width() - 500) // 2
        new_y = app.winfo_y() + (app.winfo_height() - 500) // 2

        settings_window.geometry(f"500x500+{new_x}+{new_y}")
        settings_window.transient(app)
        settings_window.grab_set()

        current_username = database.get_username(user_id)
        current_password = database.get_password(user_id)
        username_var = StringVar()
        username_var.set(current_username)
        password_var = StringVar()
        password_var.set(current_password)

        CTkLabel(master=settings_window, text="Change Username").pack(pady=10)
        username_entry = CTkEntry(master=settings_window, placeholder_text="new username", textvariable=username_var)
        username_entry.pack(pady=10)

        CTkLabel(master=settings_window, text="Change Password").pack(pady=10)
        password_entry = CTkEntry(master=settings_window, placeholder_text="new password", textvariable=password_var)
        password_entry.pack(pady=10)

        def save_changes():
            database.save_user(user_id, username_entry.get(), password_entry.get())
            messagebox.showinfo("Saved Changes", "Save changes successfully")

        save_button = CTkButton(master=settings_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)

    def add_task(task_id, task_text):
        var = IntVar()
        checkbox_text = f"{task_text}"
        checkbox = CTkCheckBox(master=checkbox_frame, text=checkbox_text, variable=var, command=update_task_status)
        checkbox.pack(anchor="w", padx=10, pady=5)
        checkboxes.append((task_id, var))
        update_task_status()


    def add_task_window():
        new_task_window = CTkToplevel(app)
        new_task_window.title("Add Task")
        new_task_window.geometry("600x350")
        new_task_window.resizable(0, 0)

        new_x = app.winfo_x() + (app.winfo_width() - 600) // 2
        new_y = app.winfo_y() + (app.winfo_height() - 350) // 2

        new_task_window.geometry(f"600x350+{new_x}+{new_y}")
        new_task_window.transient(app)
        new_task_window.grab_set()

        add_top_label = CTkLabel(master=new_task_window, text="Add Task", font=("Arial", 30, "bold"))
        add_top_label.pack(padx=50 , pady=2, anchor="w")

        add_top_frame = CTkFrame(master=new_task_window, width=500, height=80)
        add_top_frame.pack(pady=10)

        # Karakter sınırı için kontrol fonksiyonu
        def limit_text_length(text):
            if len(text) > 40:
                task_entry.delete(40, 'end')

        task_entry = CTkEntry(master=add_top_frame, placeholder_text="Enter a task...", width=300)
        task_entry.place(x=20, y=25)

        task_entry.bind("<KeyRelease>", lambda event: limit_text_length(task_entry.get()))

        is_favorite_var = IntVar(value=0)
        normal_star_image_data = Image.open("normal_star.png")
        favorite_image_data = Image.open("favorite_star.png")
        normal_star_image = CTkImage(dark_image=normal_star_image_data, light_image=normal_star_image_data, size=(20, 20))
        favorite_star_image = CTkImage(dark_image=favorite_image_data, light_image=favorite_image_data, size=(20, 20))
        CTkLabel(master=add_top_frame, text="", image=normal_star_image).place(x=465, y=7)
        CTkLabel(master=add_top_frame, text="", image=favorite_star_image).place(x=465, y=42)

        CTkRadioButton(master=add_top_frame, text="Normal", variable=is_favorite_var, value=0).place(x=340, y=10)
        CTkRadioButton(master=add_top_frame, text="Add to favorites", variable=is_favorite_var, value=1).place(x=340, y=45)

        def open_calendar():
            calendar_window = CTkToplevel(app)
            calendar_window.title("Calendar")
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
        selected_due_date.set("No Date Selected")

        def save_task():
            task_name = task_entry.get()
            is_favorite = is_favorite_var.get()
            repeat_interval = selected_repeater_option.get()
            due_date = selected_due_date.get()
            reminder_time = selected_reminder_option.get()

            if task_name:
                if reminder_time.startswith("Today"):
                    reminder_time = (datetime.now() + timedelta(minutes=2)).replace(second=0, microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                elif reminder_time.startswith("Tomorrow"):
                    reminder_time = (datetime.now() + timedelta(days=1)).replace(hour=3, minute=0, second=0, microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                else:
                    reminder_time = ""
                if repeat_interval != "No Repeater" and due_date == "No Date Selected":
                    messagebox.showerror("Error", "You have to choose due date for your repeated task")
                    return
                task_id = database.add_task_to_db(user_id, task_name, is_favorite, due_date, repeat_interval, reminder_time)
                add_task(task_id, task_name)
                refresh_task_list()
                update_task_status()
                new_task_window.destroy()

        date_options = ["No Due Date", "Today", "Tomorrow", "Next Week", "Pick a Date"]
        selected_date_option = StringVar(value=date_options[0])

        def handle_date_option(choice):
            if choice == "No Due Date":
                selected_due_date.set("No Date Selected")
            elif choice == "Today":
                selected_due_date.set(datetime.today().strftime("%d.%m.%Y"))
            elif choice == "Tomorrow":
                selected_due_date.set((datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y"))
            elif choice == "Next Week":
                selected_due_date.set((datetime.today() + timedelta(weeks=1)).strftime("%d.%m.%Y"))
            elif choice == "Pick a Date":
                open_calendar()

        options_frame = CTkFrame(master=new_task_window, width=500, height=70)
        options_frame.pack(pady=10)

        date_menu = CTkOptionMenu(options_frame, values=date_options, command=handle_date_option,
                                  variable=selected_date_option)
        date_menu.place(x=20, y=20)

        repeater_options = ["No Repeater", "Every Day", "Every Week"]
        selected_repeater_option = StringVar(value=repeater_options[0])

        repeater_menu = CTkOptionMenu(options_frame, values=repeater_options, variable=selected_repeater_option)
        repeater_menu.place(x=180, y=20)

        # reminder button functions
        now = datetime.now()
        three_hours_later = now + timedelta(minutes=2)
        three_hours_later = three_hours_later.replace(second=0, microsecond=0)
        today_option = three_hours_later.strftime("Today %H:%M")

        tomorrow = now + timedelta(days=1)
        tomorrow_morning = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        tomorrow_option = tomorrow_morning.strftime("Tomorrow %H:%M")

        next_week_option = (tomorrow_morning + timedelta(weeks=1)).strftime("Next Week %H:%M")

        reminder_options = ["No Reminder", today_option, tomorrow_option, next_week_option]
        selected_reminder_option = StringVar(value=reminder_options[0])

        reminder_menu = CTkOptionMenu(options_frame, values=reminder_options, variable=selected_reminder_option)
        reminder_menu.place(x=340, y=20)

        selected_date_label = CTkLabel(master=new_task_window, textvariable=selected_due_date)
        selected_date_label.pack(pady=5)

        save_button = CTkButton(master=new_task_window, text="Save Task", command=save_task)
        save_button.pack(pady=20)

    def sort_tasks(tasks, criteria):
        if criteria == "Sort by Favorite":
            tasks.sort(key=lambda x: x[3], reverse=True)
        elif criteria == "Sort by Due Date":
            tasks.sort(key=lambda x: datetime.strptime(x[4], "%d.%m.%Y") if x[4] != "No Date Selected" else datetime.max)
        elif criteria == "Sort Alphabetically":
            tasks.sort(key=lambda x: x[1].lower())
        return tasks

    def refresh_task_list(criteria=None):
        for widget in checkbox_frame.winfo_children():
            widget.destroy()

        global task_list
        task_list = database.get_tasks_from_db(user_id)
        checkboxes.clear()

        if criteria:
            task_list = sort_tasks(task_list, criteria)

        for task_id, task_text, task_status, is_favorite, selected_due_date, repeat_interval, reminder_time in task_list:
            total_length = 55
            task_text_length = len(task_text)
            display_text = task_text

            if repeat_interval:
                repeater_length = len(repeat_interval)
                repeater_text = repeat_interval

            if is_favorite:
                display_text += " ★"
                total_length = 52
            space = total_length - task_text_length - repeater_length

            for i in range(space):
                display_text += " "



            if selected_due_date != "No Date Selected":
                display_text += f"{repeater_text}  {selected_due_date}"



            var = IntVar(value=task_status)
            checkbox = CTkCheckBox(master=checkbox_frame, text=display_text, variable=var, font=("JetBrains Mono", 11, "bold"), command=update_task_status)
            checkbox.pack(anchor="w", padx=10, pady=5)
            checkboxes.append((task_id, var))

    def remove_task_window():
        remove_window = CTkToplevel(app)
        remove_window.title("Remove Task")
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
        for task_id, task_text, task_status, is_favorite, due_date, repeat_interval, reminder_time in task_list:
            var = IntVar()
            if is_favorite:
                task_text += " ★"
            remove_checkbox = CTkCheckBox(master=remove_frame, text=task_text, variable=var)
            remove_checkbox.pack(anchor="w", padx=10, pady=5)
            remove_vars.append((task_id, var))

        def remove_selected_tasks():
            global task_list, checkboxes
            task_ids_to_remove = [task_id for task_id, var in remove_vars if var.get() == 1]

            for task_id in task_ids_to_remove:
                database.remove_task_from_db(task_id)

            refresh_task_list()
            update_task_status()
            remove_window.destroy()

        remove_button = CTkButton(master=remove_window, text="Remove Selected Tasks", command=remove_selected_tasks)
        remove_button.pack(pady=10)

        CTkButton(master=remove_window, text="Remove Selected Tasks", command=remove_selected_tasks).pack(pady=10)

    # günlük tamamlanmış görevleri silme
    def schedule_task_removal():
        now = datetime.now()
        next_time = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
        delay = (next_time - now).total_seconds()
        threading.Timer(delay, task_removal_wrapper).start()

    def task_removal_wrapper():
        database.repeat_tasks()
        database.remove_completed_tasks()
        schedule_task_removal()



    def schedule_reminder_check():
        database.check_reminders_and_notify()
        app.after(60000, schedule_reminder_check)

    schedule_reminder_check()
    schedule_task_removal()
    refresh_task_list()
    update_task_status()
    app.mainloop()

login_window()
