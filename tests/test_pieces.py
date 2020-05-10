import unittest
from chess_game.pieces import King


class TestPieces(unittest.TestCase):
    def test_king(self):
        self.assertTrue(King('white').is_legal_move(0, 0, 1, 1))


if __name__ == '__main__':
    unittest.main()
