import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import csv, os

class StudentManager:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Student Records")
        self.win.geometry("1050x650")
        self.build()
        self.load()

    def build(self):
        self.fields = {}

        # ---------- FORM ----------
        form = tk.Frame(self.win)
        form.pack(pady=10)

        for i, f in enumerate(["Name","Roll","Department","Year","Email"]):
            tk.Label(form, text=f).grid(row=i, column=0, sticky="w")
            e = tk.Entry(form, width=32)
            e.grid(row=i, column=1, padx=10, pady=4)
            self.fields[f] = e

        # ---------- BUTTONS ----------
        btn = tk.Frame(form)
        btn.grid(row=6, column=0, columnspan=4, pady=10)

        for t,c,p in [
            ("Add", self.add,5),
            ("Update", self.update,5),
            ("Delete", self.delete,15),
            ("Export CSV", self.export,5)
        ]:
            tk.Button(btn, text=t, width=12, command=c).pack(side="left", padx=p)

        # ---------- FILTER ----------
        filter_frame = tk.LabelFrame(self.win, text="Filter Records")
        filter_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(filter_frame, text="Filter By:").pack(side="left", padx=5)

        self.filter_field = ttk.Combobox(
            filter_frame,
            values=["Name", "Roll", "Department", "Year"],
            state="readonly",
            width=15
        )
        self.filter_field.current(0)
        self.filter_field.pack(side="left", padx=5)

        self.filter_value = tk.Entry(filter_frame, width=25)
        self.filter_value.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)\
            .pack(side="left", padx=5)

        tk.Button(filter_frame, text="Clear Filter", command=self.load)\
            .pack(side="left", padx=5)

        # ---------- SORT ----------
        sort_frame = tk.LabelFrame(self.win, text="Sort Records")
        sort_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(sort_frame, text="Sort By:").pack(side="left", padx=5)

        self.sort_field = ttk.Combobox(
            sort_frame,
            values=["Name", "Roll", "Department", "Year"],
            state="readonly",
            width=15
        )
        self.sort_field.current(0)
        self.sort_field.pack(side="left", padx=5)

        self.sort_order = ttk.Combobox(
            sort_frame,
            values=["Ascending", "Descending"],
            state="readonly",
            width=12
        )
        self.sort_order.current(0)
        self.sort_order.pack(side="left", padx=5)

        tk.Button(sort_frame, text="Apply Sort", command=self.apply_sort)\
            .pack(side="left", padx=10)

        # ---------- TABLE ----------
        self.table = ttk.Treeview(
            self.win,
            columns=("ID","Name","Roll","Department","Year","Email"),
            show="headings"
        )

        for c in self.table["columns"]:
            self.table.heading(c, text=c)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.fill)

    # ---------- LOAD ----------
    def load(self):
        self.table.delete(*self.table.get_children())
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        for r in cur.fetchall():
            self.table.insert("", "end", values=r)
        conn.close()

    # ---------- CRUD ----------
    def add(self):
        data = [e.get().strip() for e in self.fields.values()]
        if "" in data:
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students(name,roll,department,year,email) VALUES(?,?,?,?,?)",
                data
            )
            conn.commit(); conn.close()
            self.load()
            for e in self.fields.values():
                e.delete(0, tk.END)
        except:
            messagebox.showerror(
                "Duplicate Roll",
                "This roll number already exists in the selected department"
            )

    def update(self):
        sel = self.table.focus()
        if not sel:
            return
        sid = self.table.item(sel)["values"][0]
        data = [e.get().strip() for e in self.fields.values()]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE students SET
            name=?, roll=?, department=?, year=?, email=?
            WHERE id=?
        """, (*data, sid))
        conn.commit(); conn.close()
        self.load()

    def delete(self):
        sel = self.table.focus()
        if not sel:
            return
        sid = self.table.item(sel)["values"][0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (sid,))
        conn.commit(); conn.close()
        self.load()

    def fill(self, _):
        sel = self.table.focus()
        if not sel:
            return
        vals = self.table.item(sel)["values"][1:]
        for e,v in zip(self.fields.values(), vals):
            e.delete(0, tk.END)
            e.insert(0, v)

    # ---------- FILTER ----------
    def apply_filter(self):
        field_map = {
            "Name": "name",
            "Roll": "roll",
            "Department": "department",
            "Year": "year"
        }

        field = field_map[self.filter_field.get()]
        value = self.filter_value.get().strip()

        self.table.delete(*self.table.get_children())

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM students WHERE {field} LIKE ?",
            (f"%{value}%",)
        )
        for r in cur.fetchall():
            self.table.insert("", "end", values=r)
        conn.close()

    # ---------- SORT ----------
    def apply_sort(self):
        field_map = {
            "Name": "name",
            "Roll": "roll",
            "Department": "department",
            "Year": "year"
        }

        field = field_map[self.sort_field.get()]
        order = "ASC" if self.sort_order.get() == "Ascending" else "DESC"

        self.table.delete(*self.table.get_children())

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM students ORDER BY {field} {order}")
        for r in cur.fetchall():
            self.table.insert("", "end", values=r)
        conn.close()

    # ---------- EXPORT ----------
    def export(self):
        os.makedirs("exports", exist_ok=True)
        path = "exports/students.csv"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        conn.close()

        with open(path,"w",newline="",encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID","Name","Roll","Department","Year","Email"])
            w.writerows(rows)
