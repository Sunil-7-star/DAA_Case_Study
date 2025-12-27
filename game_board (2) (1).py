
# Grid Generation, Difficulty Handling & Board UI

import tkinter as tk
from logic_rules import RuleEngine
from ai_engine import GreedyAI
import random, copy

WHITE="white"; BLACK="black"; HINT="yellow"

class GameBoard(RuleEngine, GreedyAI):
    def __init__(self, root, size, difficulty):
        self.root = root
        self.grid_size = size
        self.difficulty = difficulty
        self.root.title("2-Player Greedy Game")

        self.numbers = self.generate_grid()
        self.board = [[WHITE]*size for _ in range(size)]
        self.buttons = [[None]*size for _ in range(size)]
        self.undo_stack=[]; self.redo_stack=[]

        self.create_board()
        self.create_controls()
        self.save_state()

    def generate_grid(self):
        grid = [random.sample(range(1,10), self.grid_size)
                for _ in range(self.grid_size)]
        dup = {"Easy":1,"Medium":3,"Hard":5}[self.difficulty]
        for _ in range(dup):
            r = random.randrange(self.grid_size)
            c1,c2 = random.sample(range(self.grid_size),2)
            grid[r][c2] = grid[r][c1]
        return grid

    def create_board(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                b=tk.Button(self.root,text=self.numbers[r][c],width=6,height=3,
                            command=lambda x=r,y=c:self.human_move(x,y))
                b.grid(row=r,column=c)
                self.buttons[r][c]=b

    def create_controls(self):
        f=tk.Frame(self.root)
        f.grid(row=self.grid_size,columnspan=self.grid_size)
        tk.Button(f,text="Hint",command=self.show_hint).pack(side="left",padx=5)
        tk.Button(f,text="Undo",command=self.undo).pack(side="left",padx=5)
        tk.Button(f,text="Redo",command=self.redo).pack(side="left",padx=5)
        tk.Button(f,text="Solve Game",command=self.solve).pack(side="left",padx=5)
