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
