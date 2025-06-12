import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time

class GomokuGUI:
    def __init__(self, root, board_size=15):
        self.root = root
        self.root.title("Gomoku Game")
        self.board_size = board_size
        self.cell_size = 30
        self.canvas_padding = 20
        self.last_move = None
        
        # Frame for the game board
        self.game_frame = tk.Frame(root)
        self.game_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame for controls and info
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        
        # Create canvas for the board
        canvas_width = board_size * self.cell_size + 2 * self.canvas_padding
        canvas_height = board_size * self.cell_size + 2 * self.canvas_padding
        self.canvas = tk.Canvas(self.game_frame, width=canvas_width, height=canvas_height, bg='#e8c090')
        self.canvas.pack()
        
        # Event binding for canvas clicks
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.clickable = True  # Flag to control when clicks are processed
        
        # Create the game board
        self._draw_board()
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Gomoku! Start a new game.")
        self.status_label = tk.Label(self.control_frame, textvariable=self.status_var, font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        # Game mode selection
        self.mode_frame = tk.LabelFrame(self.control_frame, text="Game Mode", padx=10, pady=10)
        self.mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.mode_var = tk.IntVar(value=1)
        tk.Radiobutton(self.mode_frame, text="Human vs AI", variable=self.mode_var, value=1).pack(anchor=tk.W)
        tk.Radiobutton(self.mode_frame, text="AI vs AI", variable=self.mode_var, value=2).pack(anchor=tk.W)
        
        # AI settings
        self.ai_frame = tk.LabelFrame(self.control_frame, text="AI Settings", padx=10, pady=10)
        self.ai_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(self.ai_frame, text="Search Depth:").grid(row=0, column=0, sticky=tk.W)
        self.depth_var = tk.IntVar(value=3)
        self.depth_dropdown = ttk.Combobox(self.ai_frame, textvariable=self.depth_var, values=[1, 2, 3, 4, 5], width=5)
        self.depth_dropdown.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        # AI algorithm selection for player 2
        tk.Label(self.ai_frame, text="AI Algorithm:").grid(row=1, column=0, sticky=tk.W)
        self.algorithm_var = tk.StringVar(value="Alpha-Beta")
        self.algorithm_dropdown = ttk.Combobox(self.ai_frame, 
                                              textvariable=self.algorithm_var, 
                                              values=["Minimax", "Alpha-Beta"], 
                                              width=10)
        self.algorithm_dropdown.grid(row=1, column=1, padx=10, sticky=tk.W)
        
        # Control buttons
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(pady=20)
        
        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset Board", command=self.reset_board)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        self.stats_frame = tk.LabelFrame(self.control_frame, text="Statistics", padx=10, pady=10)
        self.stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.player_x_wins = tk.StringVar(value="Player X (Human): 0")
        self.player_o_wins = tk.StringVar(value="Player O (AI): 0")
        self.draws = tk.StringVar(value="Draws: 0")
        
        tk.Label(self.stats_frame, textvariable=self.player_x_wins).pack(anchor=tk.W)
        tk.Label(self.stats_frame, textvariable=self.player_o_wins).pack(anchor=tk.W)
        tk.Label(self.stats_frame, textvariable=self.draws).pack(anchor=tk.W)
        
        # Board representation (for game logic)
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.game_engine = None
        self.current_player = 'X'
        self.winner = None
        
        # Stats tracking
        self.stats = {'X': 0, 'O': 0, 'DRAW': 0}
    
    def _draw_board(self):
        # Clear previous board
        self.canvas.delete("all")
        
        # Draw grid lines
        for i in range(self.board_size):
            # Horizontal lines
            y = self.canvas_padding + i * self.cell_size
            self.canvas.create_line(
                self.canvas_padding, y, 
                self.canvas_padding + (self.board_size - 1) * self.cell_size, y,
                width=1
            )
            
            # Vertical lines
            x = self.canvas_padding + i * self.cell_size
            self.canvas.create_line(
                x, self.canvas_padding, 
                x, self.canvas_padding + (self.board_size - 1) * self.cell_size,
                width=1
            )
        
        # Draw special intersection points (for 19x19 boards)
        if self.board_size == 19:
            for x, y in [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]:
                self._draw_special_point(x, y)
        elif self.board_size == 15:
            for x, y in [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]:
                self._draw_special_point(x, y)
    
    def _draw_special_point(self, x, y):
        # Draw a small filled circle at the specified grid intersection
        cx = self.canvas_padding + x * self.cell_size
        cy = self.canvas_padding + y * self.cell_size
        self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill='black')
    
    def _draw_stone(self, row, col, player):
        x = self.canvas_padding + col * self.cell_size
        y = self.canvas_padding + row * self.cell_size
        
        # Draw the stone
        color = 'black' if player == 'X' else 'white'
        outline_color = 'white' if player == 'X' else 'black'
        
        stone_id = self.canvas.create_oval(
            x - self.cell_size/2 + 2, 
            y - self.cell_size/2 + 2, 
            x + self.cell_size/2 - 2, 
            y + self.cell_size/2 - 2, 
            fill=color, 
            outline=outline_color,
            width=1,
            tags="stone"
        )
        
        # Highlight the last move
        if self.last_move:
            last_row, last_col = self.last_move
            last_x = self.canvas_padding + last_col * self.cell_size
            last_y = self.canvas_padding + last_row * self.cell_size
            self.canvas.delete("highlight")
            
        self.canvas.create_rectangle(
            x - self.cell_size/2 + 1,
            y - self.cell_size/2 + 1,
            x + self.cell_size/2 - 1,
            y + self.cell_size/2 - 1,
            outline='red',
            width=2,
            tags="highlight"
        )
        
        self.last_move = (row, col)
        self.board[row][col] = player
    
    def on_canvas_click(self, event):
        if not self.clickable or self.winner or self.mode_var.get() == 2:
            return  # Ignore clicks when not clickable or game is over or AI vs AI mode
        
        # Convert click coordinates to board position
        col = round((event.x - self.canvas_padding) / self.cell_size)
        row = round((event.y - self.canvas_padding) / self.cell_size)
        
        # Check if valid position
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return
        
        # Check if the cell is empty
        if self.board[row][col] != ' ':
            return
        
        # Make the human move
        self._make_move(row, col, 'X')
        
        # Check for winner
        if self.check_winner(row, col):
            self.winner = 'X'
            self.status_var.set("Player X wins!")
            self.stats['X'] += 1
            self.update_stats()
            return
        
        # Check for draw
        if self._is_board_full():
            self.winner = 'DRAW'
            self.status_var.set("It's a draw!")
            self.stats['DRAW'] += 1
            self.update_stats()
            return
        
        # AI's turn
        self.status_var.set("AI is thinking...")
        self.root.update()
        
        # Disable clicks while AI is thinking
        self.clickable = False
        
        # Schedule AI move after a short delay (so UI remains responsive)
        self.root.after(100, self.make_ai_move)
    
    def make_ai_move(self):
        # This would normally call your AI algorithm
        # For now we'll just make a simple implementation
        
        # Get the best move from the AI algorithm
        from ai.minimax import Minimax
        from ai.alphabeta import AlphaBeta
        
        depth = self.depth_var.get()
        algorithm = self.algorithm_var.get()
        
        if algorithm == "Minimax":
            ai = Minimax()
        else:  # Alpha-Beta
            ai = AlphaBeta()
        
        # Create a board representation for the AI
        from game.board import Board
        ai_board = Board(self.board_size)
        ai_board.board = [row[:] for row in self.board]
        
        # Get AI's move
        row, col = ai.get_best_move(ai_board, 'O', depth)
        
        # Make the AI move
        self._make_move(row, col, 'O')
        
        # Check for winner
        if self.check_winner(row, col):
            self.winner = 'O'
            self.status_var.set("Player O (AI) wins!")
            self.stats['O'] += 1
            self.update_stats()
        # Check for draw
        elif self._is_board_full():
            self.winner = 'DRAW'
            self.status_var.set("It's a draw!")
            self.stats['DRAW'] += 1
            self.update_stats()
        else:
            self.status_var.set("Your turn")
        
        # Re-enable clicks
        self.clickable = True
    
    def _make_move(self, row, col, player):
        self._draw_stone(row, col, player)
        self.board[row][col] = player
    
    def update_stats(self):
        self.player_x_wins.set(f"Player X (Human): {self.stats['X']}")
        self.player_o_wins.set(f"Player O (AI): {self.stats['O']}")
        self.draws.set(f"Draws: {self.stats['DRAW']}")
    
    def check_winner(self, row, col):
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, and both diagonals
        
        for dr, dc in directions:
            count = 1  # Count the stone itself
            
            # Check in one direction
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if not (0 <= r < self.board_size and 0 <= c < self.board_size) or self.board[r][c] != player:
                    break
                count += 1
            
            # Check in the opposite direction
            for i in range(1, 5):
                r, c = row - dr * i, col - dc * i
                if not (0 <= r < self.board_size and 0 <= c < self.board_size) or self.board[r][c] != player:
                    break
                count += 1
            
            if count >= 5:
                return True
        
        return False
    
    def _is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def reset_board(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self._draw_board()
        self.winner = None
        self.last_move = None
        self.current_player = 'X'
        self.status_var.set("Board reset. Start a new game.")
    
    def new_game(self):
        self.reset_board()
        
        if self.mode_var.get() == 1:  # Human vs AI
            self.status_var.set("New game started. You go first (X).")
        else:  # AI vs AI
            self.status_var.set("AI vs AI game started.")
            self.ai_vs_ai_game()
    
    def ai_vs_ai_game(self):
        if self.winner or self._is_board_full():
            return
        
        # Create AI instances
        from ai.minimax import Minimax
        from ai.alphabeta import AlphaBeta
        
        minimax = Minimax()
        alphabeta = AlphaBeta()
        depth = self.depth_var.get()
        
        # Create board for AI
        from game.board import Board
        ai_board = Board(self.board_size)
        ai_board.board = [row[:] for row in self.board]
        
        # Get current player and make move
        player = self.current_player
        self.status_var.set(f"AI ({player}) is thinking...")
        self.root.update()
        
        # Choose AI algorithm based on player
        if player == 'X':
            ai = minimax
            algorithm_name = "Minimax"
        else:
            ai = alphabeta
            algorithm_name = "Alpha-Beta"
        
        # Get and make AI move
        row, col = ai.get_best_move(ai_board, player, depth)
        self._make_move(row, col, player)
        
        self.status_var.set(f"AI ({player}, {algorithm_name}) placed at ({row}, {col})")
        
        # Check for winner
        if self.check_winner(row, col):
            self.winner = player
            self.status_var.set(f"Player {player} ({algorithm_name}) wins!")
            self.stats[player] += 1
            self.update_stats()
            return
        
        # Check for draw
        if self._is_board_full():
            self.winner = 'DRAW'
            self.status_var.set("It's a draw!")
            self.stats['DRAW'] += 1
            self.update_stats()
            return
        
        # Switch player
        self.current_player = 'O' if player == 'X' else 'X'
        
        # Schedule next AI move after a delay
        self.root.after(1000, self.ai_vs_ai_game)

def setup_gui():
    root = tk.Tk()
    board_size = simpledialog.askinteger("Board Size", "Enter board size (recommended: 15 or 19):", 
                                        initialvalue=15, minvalue=5, maxvalue=19)
    if not board_size:  # User cancelled
        board_size = 15
        
    app = GomokuGUI(root, board_size)
    
    # Center window on screen
    window_width = board_size * app.cell_size + 2 * app.canvas_padding + 300  # Extra space for controls
    window_height = board_size * app.cell_size + 2 * app.canvas_padding + 40
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    return root, app

if __name__ == "__main__":
    root, app = setup_gui()
    root.mainloop()