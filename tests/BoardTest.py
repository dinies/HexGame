from context import src
from src import board as Board
from src import cell as Cell
import unittest


class TestBoardProperties(unittest.TestCase):

    def test_create_empty_board(self):
        emptyBoard = Board.Board(0, 0)
        self.assertEqual(len(emptyBoard._board), 0)

    def test_create_small_board(self):
        smallBoard = Board.Board(2, 3)
        self.assertEqual(len(smallBoard._board), 2)
        self.assertEqual(len(smallBoard._board[0]), 3)
        self.assertTrue(smallBoard.hasCell(Cell(0, 0)))
        self.assertTrue(smallBoard.hasCell(Cell(1, 0)))
        self.assertTrue(smallBoard.hasCell(Cell(0, 1)))
        self.assertTrue(smallBoard.hasCell(Cell(1, 1)))
        self.assertTrue(smallBoard.hasCell(Cell(0, 2)))
        self.assertTrue(smallBoard.hasCell(Cell(1, 2)))

    def test_neighbours_of_cell(self):
        smallBoard = Board.Board(2, 3)
        fromBottomLeftCorner = smallBoard.findNeighbours((0, 0))
        self.assertEqual(len(fromBottomLeftCorner), 3)
        self.assertTrue(Cell(0, 1) in fromBottomLeftCorner)
        self.assertTrue(Cell(1, 0) in fromBottomLeftCorner)
        self.assertTrue(Cell(1, 1) in fromBottomLeftCorner)
        fromBottomRightCorner = smallBoard.findNeighbours((1, 0))
        self.assertEqual(len(fromBottomRightCorner), 2)
        self.assertTrue(Cell(0, 0) in fromBottomRightCorner)
        self.assertTrue(Cell(1, 1) in fromBottomRightCorner)
        fromLeftEdge = smallBoard.findNeighbours((0, 1))
        self.assertEqual(len(fromLeftEdge), 4)
        self.assertTrue(Cell(0, 0) in fromLeftEdge)
        self.assertTrue(Cell(1, 1) in fromLeftEdge)
        self.assertTrue(Cell(1, 2) in fromLeftEdge)
        self.assertTrue(Cell(0, 2) in fromLeftEdge)
        mediumBoard = Board.Board(3, 3)
        fromCentre = mediumBoard.findNeighbours((1, 1))
        self.assertEqual(len(fromLeftEdge), 6)
        self.assertTrue(Cell(0, 0) in fromCentre)
        self.assertTrue(Cell(1, 0) in fromCentre)
        self.assertTrue(Cell(0, 1) in fromCentre)
        self.assertTrue(Cell(2, 1) in fromCentre)
        self.assertTrue(Cell(1, 2) in fromCentre)
        self.assertTrue(Cell(2, 2) in fromCentre)


if __name__ == '__main__':
    unittest.main()
