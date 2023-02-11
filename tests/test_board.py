from context import src
from src import board as Board
from src import cell as Cell
import unittest


class TestBoardProperties(unittest.TestCase):

    def test_create_empty_board(self):
        empty_board = Board.Board(0, 0)
        self.assertEqual(len(empty_board._board), 0)

    def test_create_small_board(self):
        small_board = Board.Board(2, 3)
        self.assertEqual(len(small_board._board), 2)
        self.assertEqual(len(small_board._board[0]), 3)
        self.assertTrue(small_board.has_cell(Cell(0, 0)))
        self.assertTrue(small_board.has_cell(Cell(1, 0)))
        self.assertTrue(small_board.has_cell(Cell(0, 1)))
        self.assertTrue(small_board.has_cell(Cell(1, 1)))
        self.assertTrue(small_board.has_cell(Cell(0, 2)))
        self.assertTrue(small_board.has_cell(Cell(1, 2)))

    def test_neighbours_of_cell(self):
        small_board = Board.Board(2, 3)
        from_bottom_left_corner = small_board.find_neighbours((0, 0))
        self.assertEqual(len(from_bottom_left_corner), 3)
        self.assertTrue(Cell(0, 1) in from_bottom_left_corner)
        self.assertTrue(Cell(1, 0) in from_bottom_left_corner)
        self.assertTrue(Cell(1, 1) in from_bottom_left_corner)
        from_bottom_right_corner = small_board.find_neighbours((1, 0))
        self.assertEqual(len(from_bottom_right_corner), 2)
        self.assertTrue(Cell(0, 0) in from_bottom_right_corner)
        self.assertTrue(Cell(1, 1) in from_bottom_right_corner)
        from_left_edge = small_board.find_neighbours((0, 1))
        self.assertEqual(len(from_left_edge), 4)
        self.assertTrue(Cell(0, 0) in from_left_edge)
        self.assertTrue(Cell(1, 1) in from_left_edge)
        self.assertTrue(Cell(1, 2) in from_left_edge)
        self.assertTrue(Cell(0, 2) in from_left_edge)
        mediumBoard = Board.Board(3, 3)
        from_centre = mediumBoard.find_neighbours((1, 1))
        self.assertEqual(len(from_left_edge), 6)
        self.assertTrue(Cell(0, 0) in from_centre)
        self.assertTrue(Cell(1, 0) in from_centre)
        self.assertTrue(Cell(0, 1) in from_centre)
        self.assertTrue(Cell(2, 1) in from_centre)
        self.assertTrue(Cell(1, 2) in from_centre)
        self.assertTrue(Cell(2, 2) in from_centre)


if __name__ == '__main__':
    unittest.main()
