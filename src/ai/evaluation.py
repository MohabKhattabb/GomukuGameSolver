class Evaluator:
    def __init__(self):
        # Score patterns
        self.five_in_a_row = 100000  # Win
        self.open_four = 10000       # Four in a row with empty spaces on both ends
        self.four = 1000             # Four in a row with one end blocked
        self.open_three = 500        # Three in a row with empty spaces on both ends
        self.three = 100             # Three in a row with one end blocked
        self.open_two = 50           # Two in a row with empty spaces on both ends
        self.two = 10                # Two in a row with one end blocked
        
    def evaluate_board(self, board, player):
        opponent = 'O' if player == 'X' else 'X'
        
        # Get raw board state
        board_state = board.get_board_state()
        size = board.size
        
        player_score = 0
        opponent_score = 0
        
        # Check horizontal patterns
        for row in range(size):
            for col in range(size - 4):
                window = [board_state[row][col+i] for i in range(5)]
                player_score += self._evaluate_window(window, player)
                opponent_score += self._evaluate_window(window, opponent)
        
        # Check vertical patterns
        for col in range(size):
            for row in range(size - 4):
                window = [board_state[row+i][col] for i in range(5)]
                player_score += self._evaluate_window(window, player)
                opponent_score += self._evaluate_window(window, opponent)
        
        # Check diagonal patterns (top-left to bottom-right)
        for row in range(size - 4):
            for col in range(size - 4):
                window = [board_state[row+i][col+i] for i in range(5)]
                player_score += self._evaluate_window(window, player)
                opponent_score += self._evaluate_window(window, opponent)
        
        # Check diagonal patterns (top-right to bottom-left)
        for row in range(size - 4):
            for col in range(4, size):
                window = [board_state[row+i][col-i] for i in range(5)]
                player_score += self._evaluate_window(window, player)
                opponent_score += self._evaluate_window(window, opponent)
        
        # Return the score difference (higher score for current player advantage)
        return player_score - opponent_score
    
    def _evaluate_window(self, window, player):
        opponent = 'O' if player == 'X' else 'X'
        empty = ' '
        
        # Count pieces
        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(empty)
        
        # Return 0 if both players have pieces in the window
        if player_count > 0 and opponent_count > 0:
            return 0
            
        # Win condition
        if player_count == 5:
            return self.five_in_a_row
            
        # Potential patterns
        if player_count == 4 and empty_count == 1:
            return self.open_four if window[0] == empty or window[4] == empty else self.four
            
        if player_count == 3 and empty_count == 2:
            return self.open_three
            
        if player_count == 2 and empty_count == 3:
            return self.open_two
            
        return 0

def potential_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

def score_move(board, move):
    # Implement scoring for a specific move
    x, y = move
    board[x][y] = 'X'  # Temporarily make the move
    evaluator = Evaluator()
    score = evaluator.evaluate_board(board, 'X')
    board[x][y] = ' '  # Undo the move
    return score