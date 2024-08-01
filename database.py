from tkinter import StringVar
import sqlite3
from datetime import datetime, timedelta
from plyer import notification
import time
def initialize_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id TEXT NOT NULL,
                      task TEXT NOT NULL,
                      status TEXT NOT NULL,
                      is_favorite INTEGER default 0,
                      due_date TEXT,
                      repeat_interval TEXT,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# kullanıcı ekleme fonk.
def add_user(username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Kullanıcı eklendi.")
    except sqlite3.IntegrityError:
        print("Kullanıcı adı zaten mevcut.")
    conn.close()

def get_username(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    username = cursor.fetchone()[0]
    conn.close()
    return username

def get_password(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
    password = cursor.fetchone()[0]
    conn.close()
    return password

def save_user(user_id, username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, user_id))
    conn.commit()
    conn.close()

# kullanıcı bilgileri kontrol fonk.
def check_credentials(username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def add_task_to_db(user_id, task, is_favorite, due_date, repeat_interval=None):
    due_date_str = due_date.get() if isinstance(due_date, StringVar) else due_date
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, task, status, is_favorite, due_date, repeat_interval) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, task, 0, is_favorite, due_date_str, repeat_interval))
    conn.commit()
    conn.close()

def get_tasks_from_db(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status, is_favorite, due_date, repeat_interval FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def remove_task_from_db(task_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def remove_completed_tasks():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE status = ?", (1,))
    conn.commit()
    conn.close()

def update_task_status_in_db(task_id, status):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

def get_past_due_tasks(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    now = datetime.now().strftime('%d.%m.%Y')
    cursor.execute("SELECT task, due_date FROM tasks WHERE user_id = ? AND due_date < ?", (user_id, now))
    past_due_tasks = cursor.fetchall()
    conn.close()
    return past_due_tasks

def remove_past_due_tasks(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    now = datetime.now().strftime('%d.%m.%Y')
    cursor.execute("SELECT id FROM tasks WHERE user_id = ? AND due_date < ?", (user_id, now))
    removed_past_due_tasks = cursor.fetchall()

    for task_id in removed_past_due_tasks:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id[0],))

    conn.commit()
    conn.close()


def repeat_tasks():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, task, is_favorite, due_date, repeat_interval FROM tasks")
    tasks = cursor.fetchall()
    today = datetime.now().strftime('%d.%m.%Y')

    for task_id, user_id, task, is_favorite, due_date, repeat_interval in tasks:
        if repeat_interval and due_date and due_date != "No Date Selected":
            due_date_dt = datetime.strptime(due_date, '%d.%m.%Y')
            next_due_date = None
            if repeat_interval == "Every Day":
                next_due_date = due_date_dt + timedelta(days=1)
            elif repeat_interval == "Every Week":
                next_due_date = due_date_dt + timedelta(weeks=1)
            pass

            if next_due_date and next_due_date.strftime("%d.%m.%Y") == today:
                cursor.execute("INSERT INTO tasks(user_id, task, status, is_favorite, due_date, repeat_interval) VALUES (?, ?, ?, ?, ?, ?)"
                               ,(user_id, task, 0, is_favorite, next_due_date.strftime("%d.%m.%Y"), repeat_interval))

    conn.commit()
    conn.close()



def check_reminders_and_notify():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cursor.execute("SELECT id, task, remimder_time FROM tasks WHERE reminder_time = ?", (now,))
    tasks = cursor.fetchall()

    for task_id, task, reminder_time in tasks:
        notification.notify(
            title="TASK REMAINDER",
            message=f"Reminder: {task} is due now.",
            timeout=10
        )
        cursor.execute("UPDATE tasks SET status = 1 WHERE id = ?", (task_id,))
        conn.commit()

    conn.close()
