import tkinter as tk
from game_board import GameBoard

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Singles - Game Setup")

        screen_width  = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        win_w = min(640, int(screen_width  * 0.70))
        win_h = min(900, int(screen_height * 0.90))
        x = (screen_width  - win_w) // 2
        y = (screen_height - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        # scrollable canvas
        canvas = tk.Canvas(root, bg="#1a1a2e", highlightthickness=0)
        sb     = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        outer = tk.Frame(canvas, bg="#1a1a2e")
        cwin  = canvas.create_window((0, 0), window=outer, anchor="nw")

        def _on_frame(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas(e):
            canvas.itemconfig(cwin, width=e.width)
        outer.bind("<Configure>", _on_frame)
        canvas.bind("<Configure>", _on_canvas)
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # content frame
        cf = tk.Frame(outer, bg="#1a1a2e")
        cf.pack(fill="both", expand=True, padx=30, pady=20)

        # title
        title_frame = tk.Frame(cf, bg="#16213e", relief="ridge", bd=3)
        title_frame.pack(fill="x", pady=(0, 20))
        tk.Label(title_frame, text="🎮 SINGLES",
                 font=("Helvetica", 36, "bold"),
                 bg="#16213e", fg="#00d9ff").pack(pady=18)
        tk.Label(title_frame, text="The Number Puzzle Challenge",
                 font=("Arial", 13, "italic"),
                 bg="#16213e", fg="#e94560").pack(pady=(0, 18))

        # all sections
        self.create_section(cf, "🎯 Select Grid Size",  self._grid_opts)
        self.create_section(cf, "⚡ Select Difficulty",  self._diff_opts)
        self.create_section(cf, "👥 Game Mode",          self._mode_opts)
        self.create_section(cf, "🧠 AI Strategy",        self._strategy_opts)

        # start button
        btn_frame = tk.Frame(cf, bg="#1a1a2e")
        btn_frame.pack(pady=30, fill="x")
        self._start_btn = tk.Button(
            btn_frame, text="⭐ START GAME ⭐",
            font=("Arial", 19, "bold"),
            bg="#00d9ff", fg="#1a1a2e",
            activebackground="#00b8d4", activeforeground="#1a1a2e",
            width=20, height=2, relief="raised", bd=6,
            cursor="hand2", command=self.start_game)
        self._start_btn.pack(pady=8)
        self._start_btn.bind("<Enter>",
            lambda e: self._start_btn.config(bg="#00b8d4", font=("Arial", 20, "bold")))
        self._start_btn.bind("<Leave>",
            lambda e: self._start_btn.config(bg="#00d9ff", font=("Arial", 19, "bold")))

        # footer
        ftr = tk.Frame(cf, bg="#1a1a2e")
        ftr.pack(pady=15, fill="x")
        tk.Label(ftr, text="Enjoy the challenge! 🧠✨",
                 font=("Arial", 11), bg="#1a1a2e", fg="#888888").pack()
        tk.Label(ftr, text="Scroll down if any section is hidden",
                 font=("Arial", 9, "italic"), bg="#1a1a2e", fg="#555555").pack(pady=(4, 0))

        root.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # section builder
    def create_section(self, parent, title, builder):
        frame = tk.Frame(parent, bg="#16213e", relief="groove", bd=3)
        frame.pack(fill="x", pady=12, padx=4)
        tk.Label(frame, text=title,
                 font=("Arial", 15, "bold"),
                 bg="#16213e", fg="#00d9ff").pack(anchor="w", padx=18, pady=(12, 8))
        inner = tk.Frame(frame, bg="#0f3460")
        inner.pack(fill="x", padx=18, pady=(0, 12))
        builder(inner)

    # shared radio helper
    def _rb(self, parent, text, var, val, col):
        tk.Radiobutton(
            parent, text=text, variable=var, value=val,
            font=("Arial", 13, "bold"),
            bg="#0f3460", fg="#ffffff",
            selectcolor="#e94560",
            activebackground="#0f3460", activeforeground="#00d9ff",
            cursor="hand2", padx=10, pady=6
        ).grid(row=0, column=col, padx=14, pady=8)

    # grid size
    def _grid_opts(self, parent):
        self.size_var = tk.IntVar(value=5)
        row = tk.Frame(parent, bg="#0f3460")
        row.pack(pady=10)
        for i, s in enumerate([4, 5, 6, 7]):
            self._rb(row, f"{s} × {s}", self.size_var, s, i)

    # difficulty
    def _diff_opts(self, parent):
        self.diff_var = tk.StringVar(value="Medium")
        row = tk.Frame(parent, bg="#0f3460")
        row.pack(pady=10)
        for i, (d, em) in enumerate([("Easy","🟢"),("Medium","🟡"),("Hard","🔴")]):
            self._rb(row, f"{em} {d}", self.diff_var, d, i)

    # game mode
    def _mode_opts(self, parent):
        self.mode_var = tk.StringVar(value="vs AI")
        row = tk.Frame(parent, bg="#0f3460")
        row.pack(pady=10)
        for i, (val, lbl) in enumerate([("vs AI","🤖 Human vs AI"),("2p","👥 2 Players")]):
            self._rb(row, lbl, self.mode_var, val, i)

    # AI strategy — clickable cards with description
    def _strategy_opts(self, parent):
        self.strategy_var = tk.StringVar(value="Divide & Conquer")

        strategies = [
            ("Greedy",
             "⚡ Greedy",
             "#e67e22",
             "Picks the move that\neliminates the most\nduplicates instantly.\nFast, not always optimal."),
            ("Divide & Conquer",
             "🔀 Divide & Conquer",
             "#2980b9",
             "Splits candidates\nrecursively to find\nthe best move.\nBalanced & efficient."),
            ("Dynamic Programming",
             "🧮 Dynamic Prog.",
             "#8e44ad",
             "Memoises game states\nfor theoretically\noptimal play.\nSlowest but smartest."),
            ("Backtracking",
             "🔙 Backtracking",
             "#16a085",
             "Explores all move\nsequences to find the\nlongest path.\nVery thorough."),
        ]

        card_row = tk.Frame(parent, bg="#0f3460")
        card_row.pack(pady=12, padx=6, fill="x")
        self._scards = {}

        for col, (val, label, accent, desc) in enumerate(strategies):
            card = tk.Frame(card_row, bg="#16213e", relief="ridge", bd=2, cursor="hand2")
            card.grid(row=0, column=col, padx=7, pady=4, sticky="nsew")
            card_row.columnconfigure(col, weight=1)

            rb = tk.Radiobutton(
                card, text=label,
                variable=self.strategy_var, value=val,
                font=("Arial", 11, "bold"),
                bg="#16213e", fg=accent,
                selectcolor="#0f3460",
                activebackground="#16213e", activeforeground=accent,
                cursor="hand2", pady=6)
            rb.pack(pady=(10, 2))

            tk.Label(card, text=desc,
                     font=("Arial", 9),
                     bg="#16213e", fg="#bbbbbb",
                     justify="center", wraplength=145).pack(padx=6, pady=(2, 12))

            self._scards[val] = (card, accent)

            # clicking anywhere on card activates it
            for widget in [card] + card.winfo_children():
                widget.bind("<Button-1>", lambda e, v=val: self.strategy_var.set(v))

        # glow border on selected card
        def _highlight(*_):
            sel = self.strategy_var.get()
            for v, (c, acc) in self._scards.items():
                if v == sel:
                    c.config(bd=3, relief="solid",
                             highlightthickness=2,
                             highlightbackground=acc,
                             highlightcolor=acc)
                else:
                    c.config(bd=1, relief="ridge",
                             highlightthickness=0)

        self.strategy_var.trace_add("write", _highlight)
        _highlight()

    # start game
    def start_game(self):
        size     = self.size_var.get()
        diff     = self.diff_var.get()
        mode     = self.mode_var.get()
        strategy = self.strategy_var.get()

        self.root.unbind_all("<MouseWheel>")
        self.root.destroy()

        game_root = tk.Tk()
        sw = game_root.winfo_screenwidth()
        sh = game_root.winfo_screenheight()
        gw = min(1000, int(sw * 0.80))
        gh = min(1050, int(sh * 0.90))
        game_root.geometry(f"{gw}x{gh}+{(sw-gw)//2}+{(sh-gh)//2}")
        game_root.configure(bg="#2c3e50")

        GameBoard(game_root, size, diff, mode, strategy)
        game_root.mainloop()
