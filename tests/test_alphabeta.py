import unittest
from ai.alphabeta import AlphaBeta
from game.board import Board

class TestAlphaBeta(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.ai = AlphaBeta()

    def test_initial_move(self):
        move = self.ai.get_best_move(self.board)
        self.assertIsNotNone(move)

    def test_move_evaluation(self):
        self.board.make_move(0, 0, 'X')
        score = self.ai.evaluate_board(self.board)
        self.assertIsInstance(score, int)

    def test_alpha_beta_pruning(self):
        self.board.make_move(0, 0, 'X')
        best_move = self.ai.get_best_move(self.board)
        self.assertIn(best_move, self.board.get_available_moves())

    def test_win_condition(self):
        self.board.make_move(0, 0, 'X')
        self.board.make_move(0, 1, 'X')
        self.board.make_move(0, 2, 'X')
        self.board.make_move(0, 3, 'X')
        self.board.make_move(0, 4, 'X')
        self.assertTrue(self.board.check_win('X'))

if __name__ == '__main__':
    unittest.main()