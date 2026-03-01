"""
Backtracking AI for Singles Puzzle

This AI uses backtracking to explore the game tree and find optimal moves.
It tries each valid move recursively and backtracks if it leads to a dead end.

Time Complexity: O(b^d) where b is branching factor, d is depth
Space Complexity: O(d) for recursion stack

Strategy:
- Try each valid move
- Recursively check if it leads to a solution
- Backtrack if no solution found
- Return the move that leads to the longest game path
"""

WHITE = "white"
BLACK = "black"

class BacktrackAI:
    def __init__(self):
        self.best_depth = 0
        self.best_move_found = None
        def best_move(self):
        """
        Find the best move using backtracking strategy.
        Returns:
            (row, col) tuple or None if no valid moves
        """
        moves = self.get_valid_moves()
        if not moves:
            return None
        # For very simple cases, just pick the first valid move
        if len(moves) == 1:
            return moves[0]
        # Score each move with backtracking
        best_move = None
        best_score = -1
        for r, c in moves:
            score = self.score_move(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
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
        def backtrack(self, depth=0, max_depth=10):
        """
        Backtracking search to find move leading to longest game.
        
        Args:
            depth: Current recursion depth
            max_depth: Maximum depth to search (prevents timeout)
        
        Returns:
            Number of moves in this branch
        """
        # Base case: no more moves available
        moves = self.get_valid_moves()
        if not moves or depth >= max_depth:
            return 0
        best_branch_length = 0
        # Try each valid move
        for r, c in moves:
            # Make the move
            old_state = self.board[r][c]
            self.board[r][c] = BLACK
            # Recursively explore
            branch_length = 1 + self.backtrack(depth + 1, max_depth)
            # Track the longest path
            if branch_length > best_branch_length:
                best_branch_length = branch_length
            # Backtrack: undo the move
            self.board[r][c] = old_state
        return best_branch_length
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
    def count_remaining_moves(self):
        """Count how many valid moves are available."""
        return len(self.get_valid_moves())
        
    def score_move(self, r, c):
        """
        Score a move based on:
        1. How many duplicates it removes
        2. How many moves remain after this move (via backtracking)
        """
        # Immediate score: duplicate count
        num = self.numbers[r][c]
        row_dups = sum(1 for j in range(self.grid_size)
                      if self.numbers[r][j] == num and self.board[r][j] == WHITE)
        col_dups = sum(1 for i in range(self.grid_size)
                      if self.numbers[i][c] == num and self.board[i][c] == WHITE)
        immediate_score = row_dups + col_dups - 2
        
        # Future score: how many moves remain after this
        old_state = self.board[r][c]
        self.board[r][c] = BLACK
        future_moves = self.backtrack(depth=0, max_depth=5)  # Limited depth for speed
        self.board[r][c] = old_state
        
        # Combined score: favor moves that keep the game going longer
        return immediate_score + (future_moves * 0.5)
def get_valid_moves(self):
        """Get all valid moves in current board state."""
        moves = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (self.board[r][c] == WHITE and 
                    self.is_duplicate(r, c) and 
                    self.valid_black(r, c)):
                    moves.append((r, c))
        return moves




