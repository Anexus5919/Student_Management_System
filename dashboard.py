import tkinter as tk
from theme import get, toggle
from database import get_connection
from student_crud import StudentManager
from analytics import Analytics

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dashboard")
        self.root.geometry("850x520")
        self.build()
        self.root.mainloop()

    def stats(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT department) FROM students")
        dept = cur.fetchone()[0]
        conn.close()
        return total, dept

    def card(self, parent, title, value, theme):
        f = tk.Frame(parent, bg=theme["card"], width=200, height=100)
        f.pack(side="left", padx=20)
        f.pack_propagate(False)
        tk.Label(f, text=title, bg=theme["card"], fg="white").pack(pady=10)
        tk.Label(f, text=value, bg=theme["card"],
                 fg="white", font=("Segoe UI", 22, "bold")).pack()

    def build(self):
        theme = get()
        self.root.configure(bg=theme["bg"])

        total, dept = self.stats()

        tk.Label(
            self.root, text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            fg=theme["fg"], bg=theme["bg"]
        ).pack(pady=15)

        stats = tk.Frame(self.root, bg=theme["bg"])
        stats.pack()
        self.card(stats, "Total Students", total, theme)
        self.card(stats, "Departments", dept, theme)

        for text, cmd, color in [
            ("Manage Students", lambda: StudentManager(self.root), theme["btn"]),
            ("Analytics Dashboard", lambda: Analytics(self.root), "#38bdf8"),
            ("Toggle Theme", self.toggle_theme, "#facc15"),
            ("Exit", self.root.destroy, "#ef4444")
        ]:
            tk.Button(
                self.root, text=text, command=cmd,
                bg=color, fg="black",
                width=30, height=2, bd=0
            ).pack(pady=8)

    def toggle_theme(self):
        toggle()
        self.root.destroy()
        Dashboard()
