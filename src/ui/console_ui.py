class ConsoleUI:
    def display_board(self, board):
        # Print column indices
        print("   " + "  ".join(str(i) for i in range(len(board))))
        print("  " + "=" * (len(board) * 3))
        
        # Print rows with indices
        for i, row in enumerate(board):
            print(f"{i} |" + " ".join(cell for cell in row))
    
    def prompt_user_move(self):
        while True:
            try:
                move = input("Enter your move (row and column): ")
                row, col = map(int, move.split())
                return row, col
            except ValueError:
                print("Invalid input. Please enter row and column as two integers separated by a space.")

    def display_winner(self, winner):
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a draw!")

    def ask_play_again(self):
        return input("Do you want to play again? (y/n): ").lower() == 'y'
        
    def display_message(self, message):
        print(message)