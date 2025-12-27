import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
import copy

WHITE = "white"
BLACK = "black"
HINT_COLOR = "yellow"

# ================= START MENU =================
class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Setup")

        self.size_var = tk.IntVar(value=5)
        self.diff_var = tk.StringVar(value="Easy")

        tk.Label(root, text="Select Grid Size", font=("Arial", 12, "bold")).pack(pady=5)
        for size in (4, 5, 6):
            tk.Radiobutton(root, text=f"{size} x {size}",
                           variable=self.size_var, value=size).pack()

        tk.Label(root, text="Select Difficulty", font=("Arial", 12, "bold")).pack(pady=10)
        for diff in ("Easy", "Medium", "Hard"):
            tk.Radiobutton(root, text=diff,
                           variable=self.diff_var, value=diff).pack()

        tk.Button(root, text="Start Game",
                  command=self.start_game,
                  bg="green", fg="white", width=15).pack(pady=15)

    def start_game(self):
        size = self.size_var.get()
        diff = self.diff_var.get()
        self.root.destroy()

        game_root = tk.Tk()
        TwoPlayerGreedyGame(game_root, size, diff)
        game_root.mainloop()


# ================= GAME CLASS =================
class TwoPlayerGreedyGame:
    def __init__(self, root, grid_size, difficulty):
        self.root = root
        self.grid_size = grid_size
        self.difficulty = difficulty
        self.game_over = False

        self.root.title(
            f"2-Player Greedy Game — {grid_size}x{grid_size} ({difficulty})"
        )

        self.numbers = self.generate_grid()
        self.board = [[WHITE]*grid_size for _ in range(grid_size)]
        self.buttons = [[None]*grid_size for _ in range(grid_size)]

        self.undo_stack = []
        self.redo_stack = []

        self.create_board()
        self.create_controls()
        self.save_state()

    # -------- GRID GENERATION --------
    def generate_grid(self):
        size = self.grid_size
        grid = [random.sample(range(1, 10), size) for _ in range(size)]
        duplicates = {"Easy": 1, "Medium": 3, "Hard": 5}[self.difficulty]

        for _ in range(duplicates):
            r = random.randrange(size)
            c1, c2 = random.sample(range(size), 2)
            grid[r][c2] = grid[r][c1]

        return grid

    # ---------------- GUI ----------------
    def create_board(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                btn = tk.Button(
                    self.root,
                    text=str(self.numbers[r][c]),
                    width=6, height=3,
                    command=lambda x=r, y=c: self.human_move(x, y)
                )
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.grid(row=self.grid_size, column=0,
                   columnspan=self.grid_size, pady=10)

        tk.Button(frame, text="Hint", bg="orange",
                  command=self.show_hint).pack(side="left", padx=5)
        tk.Button(frame, text="Undo", bg="lightblue",
                  command=self.undo).pack(side="left", padx=5)
        tk.Button(frame, text="Redo", bg="lightgreen",
                  command=self.redo).pack(side="left", padx=5)
        tk.Button(frame, text="Solve Game", bg="pink",
                  command=self.solve_game).pack(side="left", padx=5)

    # ---------------- STATE ----------------
    def save_state(self):
        self.undo_stack.append(copy.deepcopy(self.board))
        self.redo_stack.clear()

    def restore_state(self, state):
        self.board = copy.deepcopy(state)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c] == BLACK:
                    self.buttons[r][c].config(bg="black", fg="white")
                else:
                    self.buttons[r][c].config(bg="SystemButtonFace", fg="black")

    def undo(self):
        if len(self.undo_stack) <= 1 or self.game_over:
            return
        self.redo_stack.append(self.undo_stack.pop())
        self.restore_state(self.undo_stack[-1])

    def redo(self):
        if not self.redo_stack or self.game_over:
            return
        state = self.redo_stack.pop(0)
        self.undo_stack.append(copy.deepcopy(state))
        self.restore_state(state)

    # ---------------- HUMAN MOVE ----------------
    def human_move(self, r, c):
        if self.game_over or self.board[r][c] != WHITE:
            return

        if not self.is_duplicate_cell_board(self.board, r, c):
            messagebox.showwarning("Invalid Move",
                                   "Only duplicate cells are allowed.")
            return

        if not self.is_valid_black(r, c):
            messagebox.showwarning("Invalid Move",
                                   "This move breaks connectivity.")
            return

        self.save_state()
        self.make_black(r, c)
        self.ai_move()

    # ---------------- AI MOVE ----------------
    def ai_move(self):
        move = self.find_best_move_on_board(self.board)

        if move is None:
            self.end_game("You Won!", "AI has no valid moves.\nCongratulations 🎉")
            return

        self.save_state()
        r, c = move
        self.make_black(r, c)

        if not self.human_has_move():
            self.end_game("Game Over", "You have no valid moves.\nBetter luck next time!")

    # ---------------- GAME END ----------------
    def end_game(self, title, msg):
        self.game_over = True
        messagebox.showinfo(title, msg)
        self.root.destroy()
        new_root = tk.Tk()
        StartMenu(new_root)
        new_root.mainloop()

    # ---------------- HINT ----------------
    def show_hint(self):
        if self.game_over:
            return
        move = self.find_best_move_on_board(self.board)
        if move is None:
            messagebox.showinfo("Hint", "No valid moves available.")
            return

        r, c = move
        btn = self.buttons[r][c]
        old = btn.cget("bg")
        btn.config(bg=HINT_COLOR)
        self.root.after(1500, lambda: btn.config(bg=old))

    # ---------------- SOLVE GAME ----------------
    def solve_game(self):
        if self.game_over:
            return

        self.undo_stack.clear()
        self.redo_stack.clear()

        start_state = copy.deepcopy(self.board)
        self.undo_stack.append(copy.deepcopy(start_state))

        temp = copy.deepcopy(self.board)
        solution = []

        while True:
            move = self.find_best_move_on_board(temp)
            if move is None:
                break
            r, c = move
            temp[r][c] = BLACK
            solution.append(copy.deepcopy(temp))

        if not solution:
            messagebox.showinfo("Solve Game", "No solution exists.")
            return

        self.redo_stack = solution
        self.restore_state(start_state)
        messagebox.showinfo("Solve Game",
                            "Solution loaded.\nClick REDO to replay.")

    # ---------------- LOGIC HELPERS ----------------
    def find_best_move_on_board(self, board):
        best = None
        best_score = 0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if board[r][c] == WHITE and self.is_duplicate_cell_board(board, r, c):
                    if self.is_valid_black_board(board, r, c):
                        score = self.duplicate_score_board(board, r, c)
                        if score > best_score:
                            best_score = score
                            best = (r, c)
        return best

    def is_duplicate_cell_board(self, board, r, c):
        num = self.numbers[r][c]
        return (
            sum(board[r][j] == WHITE and self.numbers[r][j] == num
                for j in range(self.grid_size)) > 1 or
            sum(board[i][c] == WHITE and self.numbers[i][c] == num
                for i in range(self.grid_size)) > 1
        )

    def duplicate_score_board(self, board, r, c):
        num = self.numbers[r][c]
        return (
            sum(board[r][j] == WHITE and self.numbers[r][j] == num
                for j in range(self.grid_size)) +
            sum(board[i][c] == WHITE and self.numbers[i][c] == num
                for i in range(self.grid_size)) - 2
        )

    def is_valid_black_board(self, board, r, c):
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if board[nr][nc] == BLACK:
                    return False

        board[r][c] = BLACK
        ok = self.white_connected_board(board)
        board[r][c] = WHITE
        return ok

    def white_connected_board(self, board):
        visited = [[False]*self.grid_size for _ in range(self.grid_size)]
        queue = deque()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if board[i][j] != BLACK:
                    queue.append((i, j))
                    visited[i][j] = True
                    break
            if queue:
                break

        count = 1
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if not visited[nr][nc] and board[nr][nc] != BLACK:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        count += 1

        total = sum(board[i][j] != BLACK
                    for i in range(self.grid_size)
                    for j in range(self.grid_size))
        return count == total

    def is_valid_black(self, r, c):
        return self.is_valid_black_board(self.board, r, c)

    def human_has_move(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (self.board[r][c] == WHITE and
                    self.is_duplicate_cell_board(self.board, r, c) and
                    self.is_valid_black(r, c)):
                    return True
        return False

    def make_black(self, r, c):
        self.board[r][c] = BLACK
        self.buttons[r][c].config(bg="black", fg="white")


# ================= RUN =================
root = tk.Tk()
StartMenu(root)

root.mainloop()
