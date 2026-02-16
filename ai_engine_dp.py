WHITE="white"
BLACK="black"
class DPAI:
  
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
