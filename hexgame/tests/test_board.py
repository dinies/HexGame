from hexgame.src.board import Board
from hexgame.src.cell import Cell
import pytest


class TestBoardProperties:

    def test_create_empty_board(self):
        empty_board = Board(0, 0)
        assert len(empty_board._board) == 0

    @pytest.mark.parametrize("test_input",
                             [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)])
    def test_create_small_board(self, test_input: tuple[int, int]):
        small_board = Board(2, 3)
        assert len(small_board._board) == 2
        assert len(small_board._board[0]) == 3
        assert small_board.has_cell(test_input)

    @pytest.mark.parametrize(
        "board_size,tile, expected",
        [
            pytest.param("small", (0, 0), {Cell(0, 1),
                                           Cell(1, 0),
                                           Cell(1, 1)}),
            pytest.param("small", (1, 0), {Cell(0, 0),
                                           Cell(1, 1)}),
            pytest.param("small", (0, 1), {Cell(0, 0),
                                           Cell(1, 1),
                                           Cell(1, 2),
                                           Cell(0, 2)}),
            pytest.param("medium", (1, 1), {Cell(0, 0),
                                            Cell(1, 0),
                                            Cell(0, 1),
                                            Cell(1, 2),
                                            Cell(2, 1),
                                            Cell(2, 2)}),

        ]

    )
    def test_neighbours_of_cell(self, board_size: str, tile: tuple[int, int],
                                expected: set[tuple[int, int]]):
        if board_size == "small":
            board = Board(2, 3)
        elif board_size == "medium":
            board = Board(3, 3)

        nbrs = board.find_neighbours(tile)
        assert nbrs == expected
