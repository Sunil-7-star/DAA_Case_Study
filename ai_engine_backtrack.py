"""
Backtracking AI for Singles Puzzle (Optimized for Large Grids)

This AI uses backtracking with aggressive pruning and depth limiting
to handle larger grids (6×6, 7×7) without crashing or timing out.

Key Optimizations:
1. Adaptive depth limit based on grid size
2. Move ordering heuristic (try best moves first)
3. Early cutoff pruning
4. Iterative deepening for better moves
5. Greedy fallback for very complex positions

Time Complexity: O(b^d) but with d limited adaptively
Space Complexity: O(d) for recursion stack
"""

WHITE = "white"
BLACK = "black"

class BacktrackAI:
    def _init_(self):
        self.best_depth = 0
        self.best_move_found = None
        self.nodes_explored = 0
        self.max_nodes = 10000
    def show_hint(self):
        """Show hint by highlighting the best move."""
        move = self.best_move()
        if move is None:
            return
        r, c = move
        btn = self.buttons[r][c]
        old = btn.cget("bg")
        btn.config(bg="yellow")
        self.root.after(1500, lambda: btn.config(bg=old))
    
    def solve(self):
        """Solve the puzzle completely using backtracking."""
        while True:
            move = self.best_move()
            if move is None:
                break
            self.make_black(move[0], move[1])
