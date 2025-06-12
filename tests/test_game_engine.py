import unittest
from game.game_engine import GameEngine
from game.board import Board
from game.constants import BOARD_SIZE

class TestGameEngine(unittest.TestCase):

    def setUp(self):
        self.game_engine = GameEngine()
        self.board = Board()

    def test_initial_board_state(self):
        self.assertEqual(self.board.get_board_state(), [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)])

    def test_valid_move(self):
        self.game_engine.make_move(0, 0, 'X')
        self.assertEqual(self.board.get_cell(0, 0), 'X')

    def test_invalid_move(self):
        self.game_engine.make_move(0, 0, 'X')
        with self.assertRaises(ValueError):
            self.game_engine.make_move(0, 0, 'O')

    def test_win_condition(self):
        for i in range(5):
            self.game_engine.make_move(i, 0, 'X')
        self.assertTrue(self.game_engine.check_win('X'))

    def test_draw_condition(self):
        # Fill the board in a way that results in a draw
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.game_engine.make_move(i, j, 'X' if (i + j) % 2 == 0 else 'O')
        self.assertTrue(self.game_engine.check_draw())

if __name__ == '__main__':
    unittest.main()