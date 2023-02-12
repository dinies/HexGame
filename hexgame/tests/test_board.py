from hexgame.src.board import Board 
from hexgame.src.cell import Cell 
import pytest


class TestBoardProperties:

    def test_create_empty_board(self):
        empty_board = Board(0, 0)
        assert len(empty_board._board) == 0

    @pytest.mark.parametrize("test_input",
                             [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)])
    def test_create_small_board(self, test_input):
        small_board = Board(2, 3)
        assert len(small_board._board) == 2
        assert len(small_board._board[0]) == 3
        assert small_board.has_cell(test_input)

    def test_neighbours_of_cell(self):
        breakpoint()
        small_board = Board(2, 3)
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
        mediumBoard = Board(3, 3)
        from_centre = mediumBoard.find_neighbours((1, 1))
        assert len(from_left_edge) == 6
        assert Cell(0, 0) in from_centre
        assert Cell(1, 0) in from_centre
        assert Cell(0, 1) in from_centre
        assert Cell(2, 1) in from_centre
        assert Cell(1, 2) in from_centre
        assert Cell(2, 2) in from_centre
