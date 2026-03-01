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
