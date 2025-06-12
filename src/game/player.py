class Player:
    def __init__(self, symbol):
        self.symbol = symbol

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_move(self, board, ui):
        while True:
            row, col = ui.prompt_user_move()
            if board.is_valid_move(row, col):
                return row, col
            ui.display_message("Invalid move. Try again.")

class AIPlayer(Player):
    def __init__(self, symbol, algorithm, depth=3):
        super().__init__(symbol)
        self.algorithm = algorithm
        self.depth = depth
    
    def get_move(self, board, ui=None):
        ui.display_message("AI is thinking...") if ui else None
        return self.algorithm.get_best_move(board, self.symbol, self.depth)