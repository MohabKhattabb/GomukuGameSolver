from game.constants import PLAYER_X, PLAYER_O

class GameEngine:
    def __init__(self, board, player1, player2, ui):
        self.board = board
        self.player1 = player1  # X
        self.player2 = player2  # O
        self.ui = ui
        self.current_player = player1

    def start_game(self):
        self.board.reset()
        game_over = False
        
        while not game_over:
            self.ui.display_board([['.' if cell == ' ' else cell for cell in row] for row in self.board.get_board_state()])
            
            # Get move from current player
            row, col = self.current_player.get_move(self.board, self.ui)
            
            # Make move
            self.board.make_move(row, col, self.current_player.symbol)
            
            # Check winner
            winner = self.board.check_winner()
            if winner:
                self.ui.display_board([['.' if cell == ' ' else cell for cell in row] for row in self.board.get_board_state()])
                if winner == 'DRAW':
                    self.ui.display_winner(None)
                else:
                    self.ui.display_winner(winner)
                game_over = True
            
            # Switch player
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        
        return self.ui.ask_play_again()
    
    def ai_vs_ai_game(self, num_games=1):
        stats = {PLAYER_X: 0, PLAYER_O: 0, 'DRAW': 0}
        
        for game in range(num_games):
            self.board.reset()
            self.ui.display_message(f"Game {game+1}/{num_games}")
            game_over = False
            
            while not game_over:
                self.ui.display_board([['.' if cell == ' ' else cell for cell in row] for row in self.board.get_board_state()])
                
                # Get move from current player (AI)
                row, col = self.current_player.get_move(self.board)
                
                # Make move
                self.board.make_move(row, col, self.current_player.symbol)
                
                # Check winner
                winner = self.board.check_winner()
                if winner:
                    self.ui.display_board([['.' if cell == ' ' else cell for cell in row] for row in self.board.get_board_state()])
                    if winner == 'DRAW':
                        self.ui.display_winner(None)
                        stats['DRAW'] += 1
                    else:
                        self.ui.display_winner(winner)
                        stats[winner] += 1
                    game_over = True
                
                # Switch player
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        
        # Display statistics
        self.ui.display_message(f"Results after {num_games} games:")
        self.ui.display_message(f"Player X (Minimax): {stats[PLAYER_X]} wins")
        self.ui.display_message(f"Player O (Alpha-Beta): {stats[PLAYER_O]} wins")
        self.ui.display_message(f"Draws: {stats['DRAW']}")
        
        return stats