import tkinter as tk
from database import init_db
from login import LoginApp

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
