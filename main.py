
import tkinter as tk
from start_menu import StartMenu

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1a1a2e")
    app=StartMenu(root)
    root.mainloop()
