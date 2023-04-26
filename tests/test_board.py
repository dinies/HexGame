from hexgame.board import Board
from hexgame.cell import Cell
from hexgame.color import Color
from hexgame.unionfind import UnionFind
import pytest


class TestBoardProperties:

    def test_create_empty_board(self):
        dim_x = 0
        dim_y = 0
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        empty_board = Board(dim_x=dim_x, dim_y=dim_y,
                            red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        assert len(empty_board._board) == 0

    def test_empty_cells_on_blank_board(self):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        small_board = Board(dim_x=dim_x, dim_y=dim_y,
                            red_conn_comp=uf_red, blue_conn_comp=uf_blue)

        for i in range(3):
            for j in range(3):
                assert small_board[i, j].is_empty

    @pytest.mark.parametrize("test_input",
                             [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)])
    def test_create_small_board(self, test_input: tuple[int, int]):
        dim_x = 2
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        small_board = Board(dim_x=dim_x, dim_y=dim_y,
                            red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        assert len(small_board._board) == 2
        assert len(small_board._board[0]) == 3
        assert small_board.has_cell(test_input)

    # __str__
    @pytest.mark.parametrize(
        "board_sizes,expected",
        [pytest.param(
            (0, 0), ''
        ),
            pytest.param(
            (3, 4), '- - - \n - - - \n  - - - \n   - - - \n'
        )]
    )
    def test__str__empty_board(
            self, board_sizes: tuple[int, int], expected: str):
        fake_uf = UnionFind([(1, 1)])
        board = Board(dim_x=board_sizes[0], dim_y=board_sizes[1],
                      red_conn_comp=fake_uf, blue_conn_comp=fake_uf)
        print(str(board))
        print(expected)
        assert str(board) == expected

    # find_neighbours

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
            dim_x = 2
            dim_y = 3
        elif board_size == "medium":
            dim_x = 3
            dim_y = 3

        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)

        nbrs = board.find_neighbours(tile)
        assert nbrs == expected

    def test_swap_rule_allowed(self):
        dim_x = 2
        dim_y = 2
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)

        assert board._swap_rule_allowed

    # place_stone

    def test_place_stone_on_empty_board(self):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        board.place_stone(1, 2, color=Color.Red)

        assert board[1, 2] == Cell(1, 2, Color.Red)

    def test_use_swap_rule(self):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        board.place_stone(1, 2, color=Color.Red)

        board.place_stone(1, 2, color=Color.Blue)
        assert board[1, 2].color == Color.Blue

    def test_place_stone_already_filled(self):
        with pytest.raises(ValueError):
            dim_x = 3
            dim_y = 3
            nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
            uf_red = UnionFind(nodes)
            uf_blue = UnionFind(nodes)
            board = Board(dim_x=dim_x, dim_y=dim_y,
                          red_conn_comp=uf_red, blue_conn_comp=uf_blue)
            board.place_stone(0, 0, color=Color.Blue)

            board.place_stone(1, 2, color=Color.Red)

            board.place_stone(1, 2, color=Color.Blue)

    def test_update_connected_comps(self):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        assert len(board.blue_conn_comp) == 9
        print(board.blue_conn_comp)
        color = Color.Red
        board.place_stone(1, 1, color)
        print(str(board))
        assert len(board.blue_conn_comp) == 9
        assert len(board.red_conn_comp) == 9
        board.place_stone(1, 2, color)
        print(str(board))
        assert len(board.blue_conn_comp) == 9
        assert len(board.red_conn_comp) == 8

    @pytest.mark.parametrize(
        "color_str, expected",
        [
            pytest.param("red",
                         (
                             [],
                             []
                         )),
            pytest.param("blue", (
                [],
                []
            ))
        ]
    )
    def test_get_borders_empty(
            self, color_str: str,
            expected: tuple[list[tuple[int, int]], list[tuple[int, int]]]):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        match color_str:
            case "red":
                color = Color.Red
            case "blue":
                color = Color.Blue
        res = board.get_borders(color)
        assert (res == expected)

    def test_has_color_won(self):
        dim_x = 3
        dim_y = 3
        nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
        uf_red = UnionFind(nodes)
        uf_blue = UnionFind(nodes)
        board = Board(dim_x=dim_x, dim_y=dim_y,
                      red_conn_comp=uf_red, blue_conn_comp=uf_blue)
        assert (not board._has_color_won(Color.Blue))
        assert (not board._has_color_won(Color.Red))
        board.place_stone(0, 0, Color.Red)
        assert (not board._has_color_won(Color.Blue))
        assert (not board._has_color_won(Color.Red))
        board.place_stone(0, 1, Color.Red)
        assert (not board._has_color_won(Color.Blue))
        assert (not board._has_color_won(Color.Red))
        board.place_stone(0, 2, Color.Red)
        assert (not board._has_color_won(Color.Blue))
        assert (board._has_color_won(Color.Red))
