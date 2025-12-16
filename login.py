import tkinter as tk
from tkinter import messagebox
from database import get_connection
from dashboard import Dashboard

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("420x300")
        self.root.configure(bg="#1e293b")
        self.root.resizable(False, False)
        self.build()

    def build(self):
        frame = tk.Frame(self.root, bg="#1e293b")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame, text="Student Management System",
            fg="white", bg="#1e293b",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        self.user = self.input(frame, "Username")
        self.pwd = self.input(frame, "Password", "*")

        tk.Button(
            frame, text="Login",
            command=self.login,
            bg="#4f46e5", fg="white",
            width=20, bd=0
        ).pack(pady=15)

    def input(self, parent, label, show=None):
        tk.Label(parent, text=label, fg="#cbd5f5", bg="#1e293b").pack(anchor="w")
        e = tk.Entry(parent, show=show, bg="#334155", fg="white",
                     insertbackground="white", relief="flat")
        e.pack(fill="x", ipady=6, pady=4)
        return e

    def login(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (self.user.get(), self.pwd.get())
        )
        ok = cur.fetchone()
        conn.close()

        if ok:
            self.root.destroy()
            Dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
