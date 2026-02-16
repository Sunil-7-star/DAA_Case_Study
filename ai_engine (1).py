WHITE="white"; BLACK="black"

class GreedyAI:
    def score(self,r,c):
        num=self.numbers[r][c]
        row=sum(self.numbers[r][j]==num and self.board[r][j]==WHITE for j in range(self.grid_size))
        col=sum(self.numbers[i][c]==num and self.board[i][c]==WHITE for i in range(self.grid_size))
        return row+col-2

    def best_move(self):
        best=None; score=0
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c]==WHITE and self.is_duplicate(r,c) and self.valid_black(r,c):
                    s=self.score(r,c)
                    if s>score:
                        score=s; best=(r,c)
        return best

    def ai_move(self):
        move=self.best_move()
        if not move: return
        self.save_state()
        self.make_black(*move)

    def show_hint(self):
        move=self.best_move()
        if not move: return
        r,c=move
        b=self.buttons[r][c]
        old=b.cget("bg")
        b.config(bg="yellow")
        self.root.after(1500,lambda:b.config(bg=old))

    def solve(self):
        while True:
            m=self.best_move()
            if not m: break
            self.make_black(*m)