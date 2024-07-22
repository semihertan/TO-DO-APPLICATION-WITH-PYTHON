import sqlite3
from datetime import datetime
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
                      date TEXT NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

#kullanıcı ekleme fonk.
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

# kullanıcı bilgileri kontrol fonk.
def check_credentials(username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def add_task_to_db(user_id, task, date, is_favorite):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO tasks (user_id, task, status, date, is_favorite) VALUES (?, ?, ?, ?, ?)", (user_id, task, 0, date, is_favorite))
    conn.commit()
    conn.close()

def get_tasks_from_db(user_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status, date, is_favorite FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def remove_task_from_db(task_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
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



