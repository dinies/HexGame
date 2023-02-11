from hexgame.src import board as Board
from hexgame.src import cell as Cell
import pytest


class TestBoardProperties:

    @pytest.fixture
    def small_board(self):
        return Board.Board(2, 3)

    @pytest.fixture
    def medium_board(self):
        return Board.Board(3, 3)

    def test_create_empty_board(self):
        empty_board = Board.Board(0, 0)
        assert len(empty_board._board) == 0

    def test_create_small_board(self, small_board):
        assert len(small_board._board) == 2
        assert len(small_board._board[0]) == 3
        assert small_board.has_cell(Cell(0, 0))
        assert small_board.has_cell(Cell(1, 0))
        assert small_board.has_cell(Cell(0, 1))
        assert small_board.has_cell(Cell(1, 1))
        assert small_board.has_cell(Cell(0, 2))
        assert small_board.has_cell(Cell(1, 2))

    def test_neighbours_of_cell(self, small_board, medium_board):
        from_bottom_left_corner = small_board.find_neighbours((0, 0))
        assert len(from_bottom_left_corner) == 3
        assert Cell(0, 1) in from_bottom_left_corner
        assert Cell(1, 0) in from_bottom_left_corner
        assert Cell(1, 1) in from_bottom_left_corner
        from_bottom_right_corner = small_board.find_neighbours((1, 0))
        assert len(from_bottom_right_corner) == 2
        assert Cell(0, 0) in from_bottom_right_corner
        assert Cell(1, 1) in from_bottom_right_corner
        from_left_edge = small_board.find_neighbours((0, 1))
        assert len(from_left_edge) == 4
        assert Cell(0, 0) in from_left_edge
        assert Cell(1, 1) in from_left_edge
        assert Cell(1, 2) in from_left_edge
        assert Cell(0, 2) in from_left_edge
        from_centre = medium_board.find_neighbours((1, 1))
        assert len(from_left_edge) == 6
        assert Cell(0, 0) in from_centre
        assert Cell(1, 0) in from_centre
        assert Cell(0, 1) in from_centre
        assert Cell(2, 1) in from_centre
        assert Cell(1, 2) in from_centre
        assert Cell(2, 2) in from_centre
