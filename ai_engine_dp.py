WHITE="white"
BLACK="black"
class DPAI:

  def __init__(self):
        self.memo = {}    
def ai_move(self):
        move = self.best_move()
        if move is None:
            return
        self.save_state()
        self.make_black(move[0], move[1])
  
  def is_winning_position(self):
        key = self.get_state_key()
        if key in self.memo:
            return self.memo[key]
        moves = self.get_valid_moves()
        if len(moves) == 0:
            self.memo[key] = False
            return False
        i = 0
        while i < len(moves):
            r, c = moves[i]
            self.board[r][c] = BLACK
            opponent_can_win = self.is_winning_position()
            self.board[r][c] = WHITE
            if opponent_can_win == False:
                self.memo[key] = True
                return True
            i += 1
        self.memo[key] = False
        return False
    def best_move(self):
        moves = self.get_valid_moves()
        if len(moves) == 0:
            return None
        i = 0
        while i < len(moves):
            r, c = moves[i]
            self.board[r][c] = BLACK
            if self.is_winning_position() == False:
                self.board[r][c] = WHITE
                return (r, c)
            self.board[r][c] = WHITE
            i += 1
        return moves[0]
  def show_hint(self):
        move = self.best_move()
        if move is None:
            return
        r, c = move
        b = self.buttons[r][c]
        old = b.cget("bg")
        b.config(bg="yellow")
        self.root.after(1500, lambda: b.config(bg=old))

    def solve(self):
        while True:
            m = self.best_move()
            if m is None:
                break
            self.make_black(m[0], m[1])

def get_state_key(self):
        key = []
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                row.append(self.board[r][c])
            key.append(tuple(row))
        return tuple(key)

    def get_valid_moves(self):
        moves = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c] == WHITE and self.is_duplicate(r, c) and self.valid_black(r, c):
                    moves.append((r, c))
        return moves
