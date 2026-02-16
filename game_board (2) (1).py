import copy
import random
import tkinter as tk
from tkinter import messagebox
from logic_rules import RuleEngine

from ai_engine import GreedyAI as AI
from ai_engine_dc import DivideConquerAI as AI     # For Divide and Conquer
from ai_engine_dp import DPAI as AI              # Uncomment for Dynamic Programming

WHITE = "white"
BLACK = "black"
HINT = "yellow"

class GameBoard(RuleEngine, AI):
    def __init__(self, root, size, difficulty, mode):
        AI.__init__(self)
        self.root = root
        self.grid_size = size
        self.difficulty = difficulty
        self.mode = mode
        self.current_player = 1
        self.scores = {1: 0, 2: 0}

        self.root.title(f"Singles - {self.mode}")
        self.root.configure(bg="#2c3e50")

        self.numbers = self.generate_grid()
        self.board = [[WHITE] * size for _ in range(size)]
        self.buttons = [[None] * size for _ in range(size)]
        self.undo_stack = []
        self.redo_stack = []

        self.create_header()
        self.create_board()
        self.create_controls()
        self.create_status_bar()
        self.save_state()
        self.update_status()

        if self.mode == "vs AI" and self.current_player == 2:
            self.root.after(600, self.ai_move)

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#34495e")
        header_frame.pack(fill="x", pady=(0, 10))
        tk.Label(header_frame, text="Singles - Competitive Game",
                 font=("Helvetica", 20, "bold"), bg="#34495e", fg="#ecf0f1").pack(pady=15)

    def generate_grid(self):
        grid = [random.sample(range(1, 10), self.grid_size) for _ in range(self.grid_size)]
        dup = {"Easy": 1, "Medium": 3, "Hard": 5}[self.difficulty]
        for _ in range(dup):
            r = random.randrange(self.grid_size)
            c1, c2 = random.sample(range(self.grid_size), 2)
            grid[r][c2] = grid[r][c1]
        return grid

    def create_board(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(pady=20)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                b = tk.Button(frame, text=str(self.numbers[r][c]), width=5, height=2,
                              font=("Arial", 16, "bold"),
                              command=lambda x=r, y=c: self.human_move(x, y),
                              bg="#ecf0f1", fg="#2c3e50", relief="raised", bd=3,
                              activebackground="#3498db", activeforeground="white")
                b.grid(row=r, column=c, padx=3, pady=3)
                
                # Fixed hover effect with proper variable capture
                def on_enter(event, row=r, col=c, btn=b):
                    if self.board[row][col] == WHITE:
                        btn.config(bg="#3498db", fg="white")
                
                def on_leave(event, row=r, col=c, btn=b):
                    if self.board[row][col] == WHITE:
                        btn.config(bg="#ecf0f1", fg="#2c3e50")
                
                b.bind("<Enter>", on_enter)
                b.bind("<Leave>", on_leave)
                self.buttons[r][c] = b
        def solve_and_return(self):
        """AI solves the puzzle and returns to start menu"""
        # Disable all buttons during solving
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.buttons[r][c].config(state="disabled")
        
        # Update status
        self.status_var.set("🤖 AI is solving the puzzle...")
        self.root.update()
        
        # Solve the puzzle with small delays to show moves
        def solve_step():
            m = self.best_move()
            if m is None:
                # Puzzle solved - show message and return to menu
                self.root.after(300, self.show_solve_complete)
                return
            
            self.make_black(m[0], m[1])
            self.root.update()
            # Schedule next move after a short delay
            self.root.after(200, solve_step)
        
        # Start solving
        self.root.after(300, solve_step)
    
    def show_solve_complete(self):
        """Show completion message and return to start menu"""
        messagebox.showinfo("Puzzle Solved! 🎉", 
                           "Well played! Try another puzzle! 🧩\n\n"
                           "Click OK to return to the main menu.")
        self.return_to_menu()
    
    def return_to_menu(self):
        """Return to the start menu"""
        self.root.destroy()
        
        # Import here to avoid circular imports
        from start_menu import StartMenu
        
        menu_root = tk.Tk()
        
        # Get screen dimensions
        screen_width = menu_root.winfo_screenwidth()
        screen_height = menu_root.winfo_screenheight()
        
        # Set window size
        window_width = min(600, int(screen_width * 0.7))
        window_height = min(800, int(screen_height * 0.8))
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        menu_root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        menu_root.configure(bg="#1a1a2e")
        
        StartMenu(menu_root)
        menu_root.mainloop()

    def check_game_over(self):
        """Check if the game is over - no more valid moves available"""
        has_move = False
        valid_moves = []
        
        # Check all white cells
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == WHITE:
                    # Check if this is a duplicate
                    is_dup = self.is_duplicate(i, j)
                    # Check if it can be validly blacked
                    can_black = self.valid_black(i, j) if is_dup else False
                    
                    if is_dup and can_black:
                        has_move = True
                        valid_moves.append((i, j, self.numbers[i][j]))
                        
        # Debug: Print valid moves (you can remove this later)
        if not has_move:
            print(f"Game Over Check: No valid moves found")
            print(f"Current board state:")
            for i in range(self.grid_size):
                row_str = ""
                for j in range(self.grid_size):
                    if self.board[i][j] == BLACK:
                        row_str += "  X  "
                    else:
                        row_str += f" {self.numbers[i][j]:2d}  "
                print(row_str)
        else:
            print(f"Valid moves available: {len(valid_moves)}")
            for r, c, num in valid_moves[:3]:  # Show first 3
                print(f"  - Position ({r},{c}) = {num}")
        
        if not has_move:
            # Game is over - show results
            if self.mode == "vs AI":
                if self.scores[1] > self.scores[2]:
                    title = "🎉 Congratulations!"
                    message = f"You Win!\n\nYour Score: {self.scores[1]} moves\nAI Score: {self.scores[2]} moves\n\nWell played! 🏆"
                elif self.scores[1] < self.scores[2]:
                    title = "Game Over"
                    message = f"AI Wins!\n\nYour Score: {self.scores[1]} moves\nAI Score: {self.scores[2]} moves\n\nBetter luck next time! 💪"
                else:
                    title = "Game Over"
                    message = f"It's a Draw!\n\nBoth players: {self.scores[1]} moves\n\nGreat match! 🤝"
            else:
                # 2-player mode
                if self.scores[1] > self.scores[2]:
                    title = "🎉 Player 1 Wins!"
                    message = f"Congratulations!\n\nPlayer 1: {self.scores[1]} moves\nPlayer 2: {self.scores[2]} moves"
                elif self.scores[1] < self.scores[2]:
                    title = "🎉 Player 2 Wins!"
                    message = f"Congratulations!\n\nPlayer 1: {self.scores[1]} moves\nPlayer 2: {self.scores[2]} moves"
                else:
                    title = "Game Over"
                    message = f"It's a Draw!\n\nBoth players: {self.scores[1]} moves"
            
            messagebox.showinfo(title, message)
            self.root.after(1000, self.return_to_menu)

    def refresh(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c] == BLACK:
                    self.buttons[r][c].config(bg="#34495e", fg="#ecf0f1", state="disabled", relief="sunken")
                else:
                    self.buttons[r][c].config(bg="#ecf0f1", fg="#2c3e50", state="normal", relief="raised")

    def undo(self):
        if len(self.undo_stack) <= 1: 
            messagebox.showinfo("Undo", "No more moves to undo!")
            return
        self.redo_stack.append(self.undo_stack.pop())
        self.board = copy.deepcopy(self.undo_stack[-1])
        self.current_player = 1
        self.refresh()
        self.update_status()

    def redo(self):
        if not self.redo_stack: 
            messagebox.showinfo("Redo", "No moves to redo!")
            return
        state = self.redo_stack.pop()
        self.undo_stack.append(copy.deepcopy(state))
        self.board = copy.deepcopy(state)
        self.current_player = 1
        self.refresh()
        self.update_status()

    def create_controls(self):
        ctrl = tk.Frame(self.root, bg="#2c3e50")
        ctrl.pack(pady=15)
        
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "width": 12,
            "height": 1,
            "relief": "raised",
            "bd": 2
        }
        
        tk.Button(ctrl, text="💡 Hint", command=self.show_hint, 
                  bg="#f39c12", fg="white", **btn_style).pack(side="left", padx=5)
        tk.Button(ctrl, text="↶ Undo", command=self.undo, 
                  bg="#e74c3c", fg="white", **btn_style).pack(side="left", padx=5)
        tk.Button(ctrl, text="↷ Redo", command=self.redo, 
                  bg="#9b59b6", fg="white", **btn_style).pack(side="left", padx=5)
        tk.Button(ctrl, text="🤖 Solve", command=self.solve_and_return, 
                  bg="#27ae60", fg="white", **btn_style).pack(side="left", padx=5)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        status_frame = tk.Frame(self.root, bg="#34495e")
        status_frame.pack(side="bottom", fill="x")
        tk.Label(status_frame, textvariable=self.status_var, font=("Arial", 13, "bold"),
                 bg="#34495e", fg="#ecf0f1", pady=12).pack()

    def update_status(self):
        turn = "🎮 Your turn" if self.mode == "vs AI" and self.current_player == 1 else \
               "🤖 AI thinking..." if self.mode == "vs AI" and self.current_player == 2 else \
               f"Player {self.current_player}'s turn"
        self.status_var.set(f"{turn}   |   Player 1: {self.scores[1]}   Player 2: {self.scores[2]}")

    def human_move(self, r, c):
        if self.board[r][c] != WHITE: return
        if self.mode == "vs AI" and self.current_player != 1: return
        if not self.is_duplicate(r, c):
            messagebox.showwarning("Invalid Move", "Only duplicate numbers can be selected!\n\n"
                                 f"The number {self.numbers[r][c]} must appear more than once "
                                 "in its row or column among white cells.")
            return
        
        # Check for adjacent black cells FIRST
        if self.has_adjacent_black(r, c):
            messagebox.showwarning("Invalid Move", "No two black squares can be adjacent!\n\n"
                                 "Black cells cannot touch horizontally or vertically.")
            return
        
        if not self.valid_black(r, c):
            messagebox.showwarning("Invalid Move", "White cells must remain connected!\n\n"
                                 "This move would isolate some white cells.")
            return

        self.save_state()
        self.make_black(r, c)
        self.scores[self.current_player] += 1
        self.current_player = 3 - self.current_player
        self.update_status()
        self.check_game_over()

        if self.mode == "vs AI" and self.current_player == 2:
            self.root.after(700, self.ai_move)

    def ai_move(self):
        if self.current_player != 2 or self.mode != "vs AI": return
        move = self.best_move()
        if not move:
            self.check_game_over()
            return
        r, c = move
        self.save_state()
        self.make_black(r, c)
        self.scores[2] += 1
        self.current_player = 1
        self.update_status()
        self.check_game_over()

    def make_black(self, r, c):
        self.board[r][c] = BLACK
        self.buttons[r][c].config(bg="#34495e", fg="#ecf0f1", state="disabled", relief="sunken")

