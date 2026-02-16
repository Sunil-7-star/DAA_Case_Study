WHITE="white"
BLACK="black"
class DivideConquerAI:
  def _find_best_move(self, candidates):
          if len(candidates) == 0:
              return None
          if len(candidates) == 1:
              return candidates[0]
  
          mid = len(candidates) // 2
          left = self._find_best_move(candidates[:mid])
          right = self._find_best_move(candidates[mid:])
  
          if left is None:
              return right
          if right is None:
              return left
  
          score_left = self.score(left[0], left[1])
          score_right = self.score(right[0], right[1])
          if score_left >= score_right:
              return left
          return right
  def best_move(self):
        candidates = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (self.board[r][c] == WHITE and 
                    self.is_duplicate(r, c) and 
                    self.valid_black(r, c)):
                    candidates.append((r, c))
        return self._find_best_move(candidates)
  def show_hint(self):
        move = self.best_move()
        if move is None:
            return
        r, c = move
        b = self.buttons[r][c]
        old = b.cget("bg")
        b.config(bg="yellow")
        self.root.after(1500, lambda: b.config(bg=old))

  def ai_move(self):
        move = self.best_move()
        if move is None:
            return
        self.save_state()
        self.make_black(move[0], move[1])

    def solve(self):
        while True:
            m = self.best_move()
            if m is None:
                break
            self.make_black(m[0], m[1])
          


