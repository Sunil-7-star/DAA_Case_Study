import tkinter as tk
from tkinter import ttk
from game_board import GameBoard

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Singles - Game Setup")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size (70% of screen or max 600x800)
        window_width = min(600, int(screen_width * 0.7))
        window_height = min(800, int(screen_height * 0.8))
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        # Create a canvas with scrollbar
        canvas = tk.Canvas(root, bg="#1a1a2e", highlightthickness=0)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        
        # Main container frame inside canvas
        main_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Configure scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Make the frame width match canvas width
            canvas_width = event.width if event else canvas.winfo_width()
            canvas.itemconfig(canvas_frame, width=canvas_width)
        
        main_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Add padding to main frame
        content_frame = tk.Frame(main_frame, bg="#1a1a2e")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Title Section
        title_frame = tk.Frame(content_frame, bg="#16213e", relief="ridge", bd=3)
        title_frame.pack(fill="x", pady=(0, 25))
        
        tk.Label(title_frame, text="🎮 SINGLES", 
                 font=("Helvetica", 38, "bold"), 
                 bg="#16213e", fg="#00d9ff").pack(pady=20)
        tk.Label(title_frame, text="The Number Puzzle Challenge", 
                 font=("Arial", 14, "italic"), 
                 bg="#16213e", fg="#e94560").pack(pady=(0, 20))

        # Grid Size Section
        self.create_section(content_frame, "🎯 Select Grid Size", 
                           self.create_grid_options)

        # Difficulty Section
        self.create_section(content_frame, "⚡ Select Difficulty", 
                           self.create_difficulty_options)

        # Game Mode Section
        self.create_section(content_frame, "👥 Game Mode", 
                           self.create_mode_options)

        # Start Button - More prominent
        button_container = tk.Frame(content_frame, bg="#1a1a2e")
        button_container.pack(pady=35, fill="x")
        
        start_btn = tk.Button(button_container, text="⭐ START GAME ⭐", 
                             font=("Arial", 20, "bold"),
                             bg="#00d9ff", fg="#1a1a2e", 
                             activebackground="#00b8d4",
                             activeforeground="#1a1a2e",
                             width=20, height=2,
                             relief="raised", bd=6,
                             cursor="hand2",
                             command=self.start_game)
        start_btn.pack(pady=10)
        
        # Hover effects for start button
        def on_enter(e):
            start_btn.config(bg="#00b8d4", font=("Arial", 21, "bold"))
        
        def on_leave(e):
            start_btn.config(bg="#00d9ff", font=("Arial", 20, "bold"))
        
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

        # Footer
        footer_frame = tk.Frame(content_frame, bg="#1a1a2e")
        footer_frame.pack(pady=20, fill="x")
        tk.Label(footer_frame, text="Enjoy the challenge! 🧠✨", 
                 font=("Arial", 12), 
                 bg="#1a1a2e", fg="#888888").pack()
        
        # Instructions
        tk.Label(footer_frame, text="Scroll down if you don't see all options", 
                 font=("Arial", 9, "italic"), 
                 bg="#1a1a2e", fg="#666666").pack(pady=(5, 0))
        
        # Update scroll region after everything is added
        root.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_section(self, parent, title, content_creator):
        """Helper method to create styled sections"""
        section_frame = tk.Frame(parent, bg="#16213e", relief="groove", bd=3)
        section_frame.pack(fill="x", pady=15, padx=5)
        
        tk.Label(section_frame, text=title, 
                 font=("Arial", 16, "bold"), 
                 bg="#16213e", fg="#00d9ff").pack(anchor="w", padx=20, pady=(15, 10))
        
        content_frame = tk.Frame(section_frame, bg="#0f3460")
        content_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        content_creator(content_frame)

    def create_grid_options(self, parent):
        """Create grid size radio buttons"""
        self.size_var = tk.IntVar(value=5)
        
        grid_frame = tk.Frame(parent, bg="#0f3460")
        grid_frame.pack(pady=12)
        
        for i, s in enumerate([4, 5, 6, 7]):
            rb = tk.Radiobutton(grid_frame, 
                               text=f"{s} × {s}", 
                               variable=self.size_var, 
                               value=s,
                               font=("Arial", 14, "bold"), 
                               bg="#0f3460", 
                               fg="#ffffff",
                               selectcolor="#e94560",
                               activebackground="#0f3460",
                               activeforeground="#00d9ff",
                               cursor="hand2",
                               padx=12, pady=8)
            rb.grid(row=0, column=i, padx=18, pady=8)

    def create_difficulty_options(self, parent):
        """Create difficulty radio buttons"""
        self.diff_var = tk.StringVar(value="Medium")
        
        diff_frame = tk.Frame(parent, bg="#0f3460")
        diff_frame.pack(pady=12)
        
        difficulties = [
            ("Easy", "🟢"),
            ("Medium", "🟡"),
            ("Hard", "🔴")
        ]
        
        for i, (d, emoji) in enumerate(difficulties):
            rb = tk.Radiobutton(diff_frame, 
                               text=f"{emoji} {d}", 
                               variable=self.diff_var, 
                               value=d,
                               font=("Arial", 14, "bold"), 
                               bg="#0f3460", 
                               fg="#ffffff",
                               selectcolor="#e94560",
                               activebackground="#0f3460",
                               activeforeground="#00d9ff",
                               cursor="hand2",
                               padx=12, pady=8)
            rb.grid(row=0, column=i, padx=22, pady=8)

    def create_mode_options(self, parent):
        """Create game mode radio buttons"""
        self.mode_var = tk.StringVar(value="vs AI")
        
        mode_frame = tk.Frame(parent, bg="#0f3460")
        mode_frame.pack(pady=12)
        
        modes = [
            ("vs AI", "🤖 Human vs AI"),
            ("2p", "👥 2 Players")
        ]
        
        for i, (value, text) in enumerate(modes):
            rb = tk.Radiobutton(mode_frame, 
                               text=text, 
                               variable=self.mode_var, 
                               value=value,
                               font=("Arial", 14, "bold"), 
                               bg="#0f3460", 
                               fg="#ffffff",
                               selectcolor="#e94560",
                               activebackground="#0f3460",
                               activeforeground="#00d9ff",
                               cursor="hand2",
                               padx=15, pady=8)
            rb.grid(row=0, column=i, padx=28, pady=8)

    def start_game(self):
        """Start the game with selected options"""
        size = self.size_var.get()
        diff = self.diff_var.get()
        mode = self.mode_var.get()
        
        # Unbind mousewheel before destroying
        self.root.unbind_all("<MouseWheel>")
        self.root.destroy()
        
        # Create game window
        game_root = tk.Tk()
        
        # Get screen dimensions for game window
        screen_width = game_root.winfo_screenwidth()
        screen_height = game_root.winfo_screenheight()
        
        # Set game window size based on grid size
        if size <= 5:
            game_width = min(900, int(screen_width * 0.75))
            game_height = min(950, int(screen_height * 0.85))
        else:
            game_width = min(1000, int(screen_width * 0.8))
            game_height = min(1050, int(screen_height * 0.9))
        
        # Center game window
        x = (screen_width - game_width) // 2
        y = (screen_height - game_height) // 2
        
        game_root.geometry(f"{game_width}x{game_height}+{x}+{y}")
        game_root.configure(bg="#2c3e50")
        GameBoard(game_root, size, diff, mode)
        game_root.mainloop()
