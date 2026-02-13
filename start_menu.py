
import tkinter as tk
from game_board import GameBoar
class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Setup")

        self.size_var = tk.IntVar(value=5)
        self.diff_var = tk.StringVar(value="Easy")
        tk.Label(root, text="Select Grid Size", font=("Arial",12,"bold")).pack(pady=5)
        for s in (4,5,6):
            tk.Radiobutton(root, text=f"{s} x {s}", variable=self.size_var, value=s).pack()

        tk.Label(root, text="Select Difficulty", font=("Arial",12,"bold")).pack(pady=10)
        for d in ("Easy","Medium","Hard"):
            tk.Radiobutton(root, text=d, variable=self.diff_var, value=d).pack()

        tk.Button(root, text="Start Game", bg="green", fg="white",
                  command=self.start_game).pack(pady=15)

    def start_game(self):
        size = self.size_var.get()
        diff = self.diff_var.get()
        self.root.destroy()
        game_root = tk.Tk()
        GameBoard(game_root, size, diff)
        game_root.mainloop()
