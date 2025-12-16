import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE (for login)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # STUDENTS TABLE
    # 🔑 Composite UNIQUE constraint (department + roll)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            email TEXT,
            UNIQUE(department, roll)
        )
    """)

    # DEFAULT ADMIN USER
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', 'admin123')
    """)

    conn.commit()
    conn.close()
