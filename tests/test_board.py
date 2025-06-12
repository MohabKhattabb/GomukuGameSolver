import unittest
from game.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_state(self):
        self.assertEqual(self.board.get_state(), [[' ' for _ in range(15)] for _ in range(15)])

    def test_place_piece(self):
        self.board.place_piece(7, 7, 'X')
        self.assertEqual(self.board.get_piece(7, 7), 'X')

    def test_invalid_place_piece(self):
        self.board.place_piece(7, 7, 'X')
        with self.assertRaises(ValueError):
            self.board.place_piece(7, 7, 'O')

    def test_check_win_condition_horizontal(self):
        for i in range(5):
            self.board.place_piece(7, i, 'X')
        self.assertTrue(self.board.check_win('X'))

    def test_check_win_condition_vertical(self):
        for i in range(5):
            self.board.place_piece(i, 7, 'X')
        self.assertTrue(self.board.check_win('X'))

    def test_check_win_condition_diagonal(self):
        for i in range(5):
            self.board.place_piece(i, i, 'X')
        self.assertTrue(self.board.check_win('X'))

    def test_check_no_win_condition(self):
        self.board.place_piece(7, 7, 'X')
        self.assertFalse(self.board.check_win('O'))

if __name__ == '__main__':
    unittest.main()