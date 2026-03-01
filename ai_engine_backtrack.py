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
