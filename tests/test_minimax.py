import unittest
from ai.minimax import Minimax
from game.board import Board

class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.minimax = Minimax()

    def test_minimax_initial_move(self):
        # Test the initial move for the AI
        best_move = self.minimax.get_best_move(self.board, depth=3)
        self.assertIsNotNone(best_move)

    def test_minimax_win_condition(self):
        # Test if Minimax can identify a winning move
        self.board.make_move(0, 0, 'X')  # Simulate a move
        self.board.make_move(1, 1, 'X')  # Simulate a move
        self.board.make_move(2, 2, 'X')  # Simulate a move
        best_move = self.minimax.get_best_move(self.board, depth=3)
        self.assertEqual(best_move, (3, 3))  # Assuming (3, 3) is the winning move

    def test_minimax_blocking_move(self):
        # Test if Minimax can block an opponent's winning move
        self.board.make_move(0, 0, 'O')  # Simulate opponent's move
        self.board.make_move(0, 1, 'O')  # Simulate opponent's move
        best_move = self.minimax.get_best_move(self.board, depth=3)
        self.assertEqual(best_move, (0, 2))  # Assuming (0, 2) is the blocking move

if __name__ == '__main__':
    unittest.main()