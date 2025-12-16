import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT UNIQUE,
        department TEXT,
        year TEXT,
        email TEXT
    )
    """)

    cur.execute(
        "INSERT OR IGNORE INTO users(username,password) VALUES('admin','admin123')"
    )

    conn.commit()
    conn.close()
