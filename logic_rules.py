from collections import deque
import copy

WHITE = "white"
BLACK = "black"

class RuleEngine:
    def save_state(self):
        self.undo_stack.append(copy.deepcopy(self.board))
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) <= 1: return
        self.redo_stack.append(self.undo_stack.pop())
        self.board = copy.deepcopy(self.undo_stack[-1])
        self.refresh()

    def redo(self):
        if not self.redo_stack: return
        state = self.redo_stack.pop(0)
        self.undo_stack.append(copy.deepcopy(state))
        self.board = copy.deepcopy(state)
        self.refresh()

    def is_duplicate(self, r, c):
        num = self.numbers[r][c]
        row_count = 0
        col_count = 0
        for j in range(self.grid_size):
            if self.numbers[r][j] == num and self.board[r][j] == WHITE:
                row_count += 1
        for i in range(self.grid_size):
            if self.numbers[i][c] == num and self.board[i][c] == WHITE:
                col_count += 1
        return row_count > 1 or col_count > 1

    def has_adjacent_black(self, r, c):
        """Check if making this cell black would create adjacent black cells"""
        # Check all 4 adjacent cells (up, down, left, right)
        # Note: diagonal adjacency is NOT checked, only horizontal and vertical
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check if the adjacent cell is within bounds and is black
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if self.board[nr][nc] == BLACK:
                    return True
        return False

    def valid_black(self, r, c):
        """Check if a cell can be validly marked as black"""
        # First check: No adjacent black cells
        if self.has_adjacent_black(r, c):
            return False
        
        # Second check: White cells must stay connected
        self.board[r][c] = BLACK
        ok = self.white_connected()
        self.board[r][c] = WHITE
        return ok

    def white_connected(self):
        """Check if all white cells form a single connected group using BFS"""
        vis = [[False] * self.grid_size for _ in range(self.grid_size)]
        q = deque()
        start_found = False
        
        # Find the first white cell to start BFS
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] != BLACK:
                    q.append((i, j))
                    vis[i][j] = True
                    start_found = True
                    break
            if start_found: break
        
        if not start_found: return True  # All cells are black
        
        cnt = 1
        # BFS to count connected white cells
        while q:
            x, y = q.popleft()
            # Check 4 adjacent cells (not diagonals)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if not vis[nx][ny] and self.board[nx][ny] != BLACK:
                        vis[nx][ny] = True
                        q.append((nx, ny))
                        cnt += 1
        
        # Count total white cells
        total_white = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] != BLACK:
                    total_white += 1
        
        # All white cells must be connected
        return cnt == total_white

    def refresh(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c] == BLACK:
                    self.buttons[r][c].config(bg="black", fg="white")
                else:
                    self.buttons[r][c].config(bg="white", fg="black")

    def make_black(self, r, c):
        self.board[r][c] = BLACK
        self.buttons[r][c].config(bg="black", fg="white")
