import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import csv, os

class StudentManager:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Student Records")
        self.win.geometry("1000x600")
        self.build()
        self.load()

    def build(self):
        self.fields = {}
        form = tk.Frame(self.win)
        form.pack(pady=10)

        for i, f in enumerate(["Name","Roll","Department","Year","Email"]):
            tk.Label(form, text=f).grid(row=i, column=0, sticky="w")
            e = tk.Entry(form, width=32)
            e.grid(row=i, column=1, padx=10, pady=4)
            self.fields[f] = e

        btn = tk.Frame(form)
        btn.grid(row=6, column=0, columnspan=4, pady=10)

        for t,c,p in [
            ("Add", self.add,5),
            ("Update", self.update,5),
            ("Delete", self.delete,15),
            ("Export CSV", self.export,5)
        ]:
            tk.Button(btn, text=t, width=12, command=c).pack(side="left", padx=p)

        search = tk.Frame(self.win)
        search.pack(pady=5)

        tk.Label(search, text="Search (Name / Roll):").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search, textvariable=self.search_var, width=30).pack(side="left")
        tk.Button(search, text="Search", command=self.search).pack(side="left", padx=5)
        tk.Button(search, text="Clear", command=self.clear).pack(side="left", padx=5)

        self.table = ttk.Treeview(
            self.win,
            columns=("ID","Name","Roll","Department","Year","Email"),
            show="headings"
        )

        for c in self.table["columns"]:
            self.table.heading(
                c, text=c,
                command=lambda col=c: self.sort(col, False)
            )

        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.fill)

    def load(self):
        self.table.delete(*self.table.get_children())
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        for r in cur.fetchall():
            self.table.insert("", "end", values=r)
        conn.close()

    def clear(self):
        self.search_var.set("")
        self.table.selection_remove(self.table.selection())
        for e in self.fields.values():
            e.delete(0, tk.END)
        self.load()

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
            conn.commit()
            conn.close()

            self.load()

            # ✅ UX FIX: clear fields after successful add
            for e in self.fields.values():
                e.delete(0, tk.END)

            self.fields["Name"].focus()

        except:
            messagebox.showerror("Error", "Roll must be unique")

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
        conn.commit()
        conn.close()
        self.load()

    def delete(self):
        sel = self.table.focus()
        if not sel:
            return
        sid = self.table.item(sel)["values"][0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (sid,))
        conn.commit()
        conn.close()
        self.load()

    def fill(self, _):
        sel = self.table.focus()
        if not sel:
            return
        vals = self.table.item(sel)["values"][1:]
        for e,v in zip(self.fields.values(), vals):
            e.delete(0, tk.END)
            e.insert(0, v)

    def search(self):
        key = self.search_var.get().strip()
        self.table.delete(*self.table.get_children())
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ? OR roll LIKE ?",
            (f"%{key}%", f"%{key}%")
        )
        for r in cur.fetchall():
            self.table.insert("", "end", values=r)
        conn.close()

    def sort(self, col, rev):
        data = [(self.table.set(k,col),k) for k in self.table.get_children("")]
        data.sort(reverse=rev)
        for i,(_,k) in enumerate(data):
            self.table.move(k,"",i)
        self.table.heading(col, command=lambda: self.sort(col, not rev))

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
