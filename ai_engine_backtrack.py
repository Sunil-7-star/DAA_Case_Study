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
    def _greedy_fallback(self, moves):
        """
        Greedy fallback for very complex positions.
        Just pick the move with highest immediate score.
        """
        best_move = None
        best_score = -1
        
        for r, c in moves:
            score = self.score_move(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        return best_move if best_move else moves[0]
    def get_depth_limit(self):
        """
        Adaptive depth limit based on grid size.
        Prevents exponential blowup on large grids.
        """
        size = self.grid_size
        if size <= 4:
            return 15  # Small grid: can search deeper
        elif size == 5:
            return 10  # Medium grid
        elif size == 6:
            return 6   # Large grid: must limit depth
        else:  # 7×7 or larger
            return 4   # Very large: shallow search only
    
    def backtrack_limited(self, depth, max_depth, cutoff):
        """
        Backtracking with depth limit and pruning.
        
        Args:
            depth: Current depth
            max_depth: Maximum depth to explore
            cutoff: Best score found so far (for pruning)
        
        Returns:
            Number of moves achievable from this state
        """
        self.nodes_explored += 1
        
        # Safety check: prevent runaway exploration
        if self.nodes_explored > self.max_nodes:
            return depth
        
        # Depth limit reached
        if depth >= max_depth:
            return depth
        
        moves = self.get_valid_moves()
        
        # Base case: no more moves
        if not moves:
            return depth
        
        # Prune if this branch can't beat current best
        # Optimistic upper bound: assume all remaining moves are valid
        optimistic_max = depth + len(moves)
        if optimistic_max <= cutoff:
            return depth  # Prune this branch
        
        # Sort moves by heuristic (explore promising moves first)
        scored_moves = [(self.score_move(r, c), r, c) for r, c in moves]
        scored_moves.sort(reverse=True)
        
        # Limit branching factor on large grids
        if len(scored_moves) > 8:
            scored_moves = scored_moves[:8]  # Only explore top 8 moves
        
        best_result = depth
        
        for score, r, c in scored_moves:
            # Make move
            self.board[r][c] = BLACK
            
            # Recurse
            result = self.backtrack_limited(depth + 1, max_depth, best_result)
            
            # Backtrack
            self.board[r][c] = WHITE
            
            # Update best
            if result > best_result:
                best_result = result
            
            # Alpha-beta style pruning
            if result >= max_depth:
                break  # Found a very good path, stop exploring
        
        return best_result
    def ai_move(self):
        """Make an AI move."""
        move = self.best_move()
        if move is None:
            return
        self.save_state()
        self.make_black(move[0], move[1])
       def best_move(self):
        """
        Find the best move using optimized backtracking.
        
        Uses iterative deepening and aggressive pruning.
        Falls back to greedy if too complex.
        """
        moves = self.get_valid_moves()
        
        if not moves:
            return None
        
        if len(moves) == 1:
            return moves[0]
        
        # For very complex positions, use greedy approach
        if len(moves) > 20:
            return self._greedy_fallback(moves)
        
        # Reset node counter
        self.nodes_explored = 0
        max_depth = self.get_depth_limit()
        
        # Score each candidate move
        best_move = None
        best_score = -1
        
        # Sort moves by heuristic
        scored_moves = [(self.score_move(r, c), r, c) for r, c in moves]
        scored_moves.sort(reverse=True)
        
        # Only evaluate top candidates on large grids
        candidates = scored_moves[:min(10, len(scored_moves))]
        
        for heur_score, r, c in candidates:
            # Make move
            self.board[r][c] = BLACK
            
            # Evaluate with limited backtracking
            depth = self.backtrack_limited(1, max_depth, best_score)
            
            # Backtrack
            self.board[r][c] = WHITE
            
            # Update best
            if depth > best_score:
                best_score = depth
                best_move = (r, c)
            
            # Stop early if we've explored too many nodes
            if self.nodes_explored > self.max_nodes:
                break
        
        # Safety fallback
        if best_move is None:
            best_move = moves[0]
        
        return best_move

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
    
    def score_move(self, r, c):
        """
        Heuristic score for move ordering.
        Higher score = more promising move (explore first).
        """
        num = self.numbers[r][c]
        # Count duplicates removed
        row_dups = sum(1 for j in range(self.grid_size)
                      if self.numbers[r][j] == num and self.board[r][j] == WHITE)
        col_dups = sum(1 for i in range(self.grid_size)
                      if self.numbers[i][c] == num and self.board[i][c] == WHITE)
        dup_score = row_dups + col_dups - 2
        
        # Prefer moves that keep more options open
        # Quick estimate: count neighbors that are white
        neighbors = 0
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < self.grid_size and 0 <= nc < self.grid_size and
                self.board[nr][nc] == WHITE):
                neighbors += 1
        
        # Higher score for removing many duplicates and having flexibility
        return dup_score * 10 + neighbors
