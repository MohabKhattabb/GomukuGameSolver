def get_user_input(prompt):
    user_input = input(prompt)
    return user_input.strip()

def validate_input(user_input, valid_options):
    if user_input in valid_options:
        return True
    return False

def get_valid_move(board_size):
    while True:
        move = get_user_input("Enter your move (row and column separated by a space): ")
        try:
            row, col = map(int, move.split())
            if 0 <= row < board_size and 0 <= col < board_size:
                return row, col
            else:
                print(f"Invalid move. Please enter numbers between 0 and {board_size - 1}.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

class UserInput:
    @staticmethod
    def get_game_mode():
        while True:
            try:
                print("1. Human vs AI")
                print("2. AI vs AI")
                mode = int(input("Select game mode (1-2): "))
                if mode in [1, 2]:
                    return mode
                print("Invalid selection. Please choose 1 or 2.")
            except ValueError:
                print("Please enter a number.")
    
    @staticmethod
    def get_board_size():
        while True:
            try:
                size = int(input("Enter board size (recommended: 15 or 19): "))
                if size > 4:  # At least 5x5 to allow someone to win
                    return size
                print("Board size must be at least 5.")
            except ValueError:
                print("Please enter a number.")
    
    @staticmethod
    def get_ai_depth():
        while True:
            try:
                depth = int(input("Enter search depth for AI (recommended: 2-4): "))
                if depth > 0:
                    return depth
                print("Depth must be a positive number.")
            except ValueError:
                print("Please enter a number.")