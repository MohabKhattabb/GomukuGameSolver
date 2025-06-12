from ai.evaluation import Evaluator

class AlphaBeta:
    def __init__(self):
        self.evaluator = Evaluator()
    
    def get_best_move(self, board, player, depth):
        opponent = 'O' if player == 'X' else 'X'
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self._get_smart_moves(board):
            row, col = move
            
            # Make the move
            board.make_move(row, col, player)
            
            # Get score from alpha-beta
            score = self._alphabeta(board, depth-1, alpha, beta, False, player, opponent)
            
            # Undo the move
            board.board[row][col] = ' '
            board.last_move = None
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
        
        return best_move
    
    def _alphabeta(self, board, depth, alpha, beta, is_maximizing, player, opponent):
        # Check if game is over or depth limit reached
        winner = board.check_winner()
        if winner == player:
            return 10000
        elif winner == opponent:
            return -10000
        elif winner == 'DRAW':
            return 0
        elif depth == 0:
            return self.evaluator.evaluate_board(board, player)
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self._get_smart_moves(board):
                row, col = move
                board.make_move(row, col, player)
                score = self._alphabeta(board, depth-1, alpha, beta, False, player, opponent)
                board.board[row][col] = ' '
                board.last_move = None
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return best_score
        else:
            best_score = float('inf')
            for move in self._get_smart_moves(board):
                row, col = move
                board.make_move(row, col, opponent)
                score = self._alphabeta(board, depth-1, alpha, beta, True, player, opponent)
                board.board[row][col] = ' '
                board.last_move = None
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best_score
    
    def _get_smart_moves(self, board):
        """Instead of considering all empty cells, focus on cells near existing pieces"""
        moves = []
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        checked = set()
        
        # If board is empty, return center position
        if all(board.board[r][c] == ' ' for r in range(board.size) for c in range(board.size)):
            center = board.size // 2
            return [(center, center)]
            
        # Consider cells that are adjacent to existing pieces
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] != ' ':
                    for dr, dc in directions:
                        for dist in range(1, 3):  # Look 1-2 cells away from existing pieces
                            new_row, new_col = row + dr * dist, col + dc * dist
                            if (0 <= new_row < board.size and 
                                0 <= new_col < board.size and 
                                board.board[new_row][new_col] == ' ' and
                                (new_row, new_col) not in checked):
                                moves.append((new_row, new_col))
                                checked.add((new_row, new_col))
        
        # If no moves found, fall back to all empty cells
        if not moves:
            moves = board.get_valid_moves()
            
        return moves