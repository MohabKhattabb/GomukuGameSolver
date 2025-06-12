# filepath: gomoku-game-solver/gomoku-game-solver/src/main.py

import sys

from game.board import Board
from game.game_engine import GameEngine
from game.player import HumanPlayer, AIPlayer
from game.constants import PLAYER_X, PLAYER_O, DEFAULT_BOARD_SIZE, DEFAULT_DEPTH
from ui.console_ui import ConsoleUI
from ui.user_input import UserInput
from ai.minimax import Minimax
from ai.alphabeta import AlphaBeta

def console_game():
    ui = ConsoleUI()
    user_input = UserInput()
    
    ui.display_message("Welcome to Gomoku Game!")
    
    # Get game mode
    game_mode = user_input.get_game_mode()
    
    # Get board size
    board_size = user_input.get_board_size()
    
    # Create board
    board = Board(size=board_size)
    
    if game_mode == 1:  # Human vs AI
        # Get AI depth
        ai_depth = user_input.get_ai_depth()
        
        # Create players
        human_player = HumanPlayer(PLAYER_X)
        ai_player = AIPlayer(PLAYER_O, AlphaBeta(), depth=ai_depth)  # Using Alpha-Beta for better AI performance
        
        # Create game engine
        game = GameEngine(board, human_player, ai_player, ui)
        
        # Start game
        while game.start_game():
            ui.display_message("Starting new game...")
    
    else:  # AI vs AI
        # Get AI depth
        ai_depth = user_input.get_ai_depth()
        
        # Create players - Minimax vs Alpha-Beta
        minimax_player = AIPlayer(PLAYER_X, Minimax(), depth=ai_depth)
        alphabeta_player = AIPlayer(PLAYER_O, AlphaBeta(), depth=ai_depth)
        
        # Create game engine
        game = GameEngine(board, minimax_player, alphabeta_player, ui)
        
        # Start AI vs AI simulation
        num_games = 5  # Default number of games to simulate
        ui.display_message(f"Starting AI vs AI simulation ({num_games} games)...")
        ui.display_message("Player X: Minimax algorithm")
        ui.display_message("Player O: Alpha-Beta pruning algorithm")
        
        game.ai_vs_ai_game(num_games)
    
    ui.display_message("Thank you for playing Gomoku!")

def gui_game():
    try:
        import tkinter as tk
        from ui.gui import setup_gui
        
        root, app = setup_gui()
        root.mainloop()
    except ImportError:
        print("Tkinter is not available. Running console version instead.")
        console_game()
    except Exception as e:
        print(f"Error running GUI: {e}")
        print("Falling back to console version.")
        console_game()

def main():
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        console_game()
    else:
        # Try GUI first, fall back to console if necessary
        gui_game()

if __name__ == "__main__":
    main()