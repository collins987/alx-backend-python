from datetime import datetime
import functools
import sqlite3  # or use mysql.connector depending on your project

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[{datetime.now()}] Finished: {func.__name__}")
        return result
    return wrapper

@log_queries
def fetch_users():
    # Simulated query using sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    conn.close()
    return rows
