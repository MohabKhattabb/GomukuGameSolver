class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.last_move = None

    def display(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for idx, row in enumerate(self.board):
            print(idx, " ".join(row))

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = player
        self.last_move = (row, col)
        return True

    def is_valid_move(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        return self.board[row][col] == ' '

    def get_valid_moves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == ' ':
                    moves.append((row, col))
        return moves

    def check_winner(self):
        if self.last_move is None:
            return None

        row, col = self.last_move
        player = self.board[row][col]

        # Check horizontal
        for c in range(max(0, col - 4), min(self.size - 4, col + 1)):
            if all(self.board[row][c + i] == player for i in range(5)):
                return player

        # Check vertical
        for r in range(max(0, row - 4), min(self.size - 4, row + 1)):
            if all(self.board[r + i][col] == player for i in range(5)):
                return player

        # Check diagonal (top-left to bottom-right)
        for i in range(-4, 1):
            r, c = row + i, col + i
            if 0 <= r <= self.size - 5 and 0 <= c <= self.size - 5:
                if all(self.board[r + j][c + j] == player for j in range(5)):
                    return player

        # Check diagonal (top-right to bottom-left)
        for i in range(-4, 1):
            r, c = row + i, col - i
            if 0 <= r <= self.size - 5 and 0 <= c + 4 < self.size:
                if all(self.board[r + j][c - j] == player for j in range(5)):
                    return player

        # Check if the board is full (draw)
        if all(self.board[r][c] != ' ' for r in range(self.size) for c in range(self.size)):
            return 'DRAW'

        return None

    def reset(self):
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None

    def get_board_state(self):
        return [row[:] for row in self.board]