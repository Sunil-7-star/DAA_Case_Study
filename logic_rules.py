

# Human Interaction & Rule Enforcement

from tkinter import messagebox
from collections import deque
import copy

WHITE="white"; BLACK="black"

class RuleEngine:
    def save_state(self):
        self.undo_stack.append(copy.deepcopy(self.board))
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack)<=1: return
        self.redo_stack.append(self.undo_stack.pop())
        self.board=copy.deepcopy(self.undo_stack[-1])
        self.refresh()

    def redo(self):
        if not self.redo_stack: return
        state=self.redo_stack.pop(0)
        self.undo_stack.append(copy.deepcopy(state))
        self.board=copy.deepcopy(state)
        self.refresh()

    def human_move(self,r,c):
        if self.board[r][c]!=WHITE: return
        if not self.is_duplicate(r,c):
            messagebox.showwarning("Invalid","Only duplicate cells allowed")
            return
        if not self.valid_black(r,c):
            messagebox.showwarning("Invalid","Connectivity broken")
            return
        self.save_state()
        self.make_black(r,c)
        self.ai_move()

    def is_duplicate(self,r,c):
        num=self.numbers[r][c]
        return sum(self.numbers[r][j]==num and self.board[r][j]==WHITE for j in range(self.grid_size))>1 or sum(self.numbers[i][c]==num and self.board[i][c]==WHITE for i in range(self.grid_size))>1

    def valid_black(self,r,c):
        self.board[r][c]=BLACK
        ok=self.white_connected()
        self.board[r][c]=WHITE
        return ok

    def white_connected(self):
        vis=[[False]*self.grid_size for _ in range(self.grid_size)]
        q=deque()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j]!=BLACK:
                    q.append((i,j)); vis[i][j]=True; break
            if q: break
        cnt=1
        while q:
            x,y=q.popleft()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx,ny=x+dx,y+dy
                if 0<=nx<self.grid_size and 0<=ny<self.grid_size:
                    if not vis[nx][ny] and self.board[nx][ny]!=BLACK:
                        vis[nx][ny]=True; q.append((nx,ny)); cnt+=1
        total=sum(self.board[i][j]!=BLACK for i in range(self.grid_size) for j in range(self.grid_size))
        return cnt==total

    def refresh(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.board[r][c]==BLACK:
                    self.buttons[r][c].config(bg="black",fg="white")
                else:
                    self.buttons[r][c].config(bg="SystemButtonFace",fg="black")

    def make_black(self,r,c):
        self.board[r][c]=BLACK
        self.buttons[r][c].config(bg="black",fg="white")
