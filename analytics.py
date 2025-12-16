import tkinter as tk
from database import get_connection

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class Analytics:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Analytics Dashboard")
        self.win.geometry("900x650")
        self.win.minsize(700, 500)   # small but safe
        self.win.configure(bg="#f8fafc")

        self.build_ui()

    def build_ui(self):
        # ---------- TITLE ----------
        tk.Label(
            self.win,
            text="Analytics Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#f8fafc"
        ).pack(pady=15)

        # ---------- DATA ----------
        total_students, departments, counts = self.fetch_data()

        # ---------- SUMMARY ----------
        summary = tk.Frame(self.win, bg="#f8fafc")
        summary.pack(pady=10)

        self.card(summary, "Total Students", total_students)
        self.card(summary, "Departments", len(departments))

        # ---------- CHART FRAME ----------
        outer = tk.LabelFrame(
            self.win,
            text="Students per Department",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            padx=10,
            pady=10
        )
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------- FIGURE ----------
        fig = Figure(figsize=(7.5, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(departments, counts)
        ax.set_title("Students per Department")
        ax.set_xlabel("Department")
        ax.set_ylabel("Number of Students")

        fig.tight_layout()

        # ---------- CANVAS ----------
        canvas = FigureCanvasTkAgg(fig, master=outer)
        canvas.draw()

        # ---------- TOOLBAR (ABOVE CANVAS – KEY FIX) ----------
        toolbar = NavigationToolbar2Tk(canvas, outer)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # ---------- CANVAS WIDGET ----------
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- DATA ----------
    def fetch_data(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM students")
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT department, COUNT(*)
            FROM students
            GROUP BY department
        """)
        data = cur.fetchall()

        conn.close()

        departments = [d[0] for d in data]
        counts = [d[1] for d in data]

        return total, departments, counts

    # ---------- SUMMARY CARD ----------
    def card(self, parent, title, value):
        frame = tk.Frame(
            parent,
            bg="#e2e8f0",
            width=220,
            height=90
        )
        frame.pack(side="left", padx=20)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg="#e2e8f0",
            font=("Segoe UI", 10)
        ).pack(pady=(15, 5))

        tk.Label(
            frame,
            text=value,
            bg="#e2e8f0",
            font=("Segoe UI", 22, "bold")
        ).pack()
