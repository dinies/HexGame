"""board.py: A board to play a game of hex on"""
from hexgame.src.cell import Cell
from hexgame.src.color import Color
from hexgame.src.unionfind import UnionFind


BOARD_DEFAULT_X_DIM = BOARD_DEFAULT_Y_DIM = int(11)

__author__ = "Gianpiero Cea"

"""
 A board is a set of exagonal cells stacked in a 2D matrix shape.
 It can be indexed similarly to a matrix with (x, y) coordinates.
 The (0,0) coordinate starts at the bottom left corner of the board.
 The x coordinate indexes horizontally (going from left to right)
 and the y vertically (going from bottom to top)
 The hexagonal cells make so that the board is slanted in a
 romboidal shape. The slanting goes to the left.
 ----------
 '         '
  '         '
   '         '
     ----------
"""


class Board:

    def __init__(
        self,
        red_conn_comp: UnionFind[tuple[int, int]],
        blue_conn_comp: UnionFind[tuple[int, int]],
        dim_x: int = BOARD_DEFAULT_X_DIM,
        dim_y: int = BOARD_DEFAULT_Y_DIM
    ) -> None:
        self.dim_x: int = dim_x
        self.dim_y: int = dim_y
        self._board: list[list[Cell]] = self._make_board(dim_x, dim_y)

        self._red_conn_comp: UnionFind[tuple[int,
                                             int]] = red_conn_comp
        self._blue_conn_comp: UnionFind[tuple[int,
                                              int]] = blue_conn_comp

    def __getitem__(self, coord: tuple) -> Cell:
        x, y = coord
        return self._board[x][y]

    def __setitem__(self, coord: tuple, val: Cell):
        x, y = coord
        # TODO: I am not liking this..check later if we should drop x,y in cell
        assert val.x == x
        assert val.y == y
        self._board[x][y] = val

    def __repr__(self) -> str:
        # TODO: change the Cell repr to be simpler
        # then change this one to make it even simpler
        return (str(self._board))

    def __str__(self) -> str:
        """
        We visualize the board as a left-slanted romboidal.
        If cell i,j is empty we visualise it with a dash,
        if is occupied by Red player we visualise it with letter R
        and if cocupeid by Blue Player we visualitse it with a letter b

        for example, for a 5X5 board:

        - - - - -
         - b - - - 
          - - - R -
           - - - b -
            - - R - -

        """
        board_str = ""

        for y in reversed(range(self.dim_y)):
            new_line = " "*(self.dim_y-y-1)
            for x in range(self.dim_x):
                cell = self[x, y]
                match cell:
                    case Cell(x, y, Color.Empty):
                        cell_str = '-'
                    case Cell(x, y, Color.Red):
                        cell_str = 'R'
                    case Cell(x, y, Color.Blue):
                        cell_str = 'b'

                new_line += cell_str + " "
            new_line += "\n"
            board_str += new_line
            # add spaces to make it slante

        return board_str

    def _make_board(self, dim_x: int, dim_y: int) -> list[list[Cell]]:
        """
        represents a dim_x * dim_y board of hexagonal cells
        """
        return [[Cell(x, y) for y in range(dim_y)] for x in range(dim_x)]

    def _update_conn_comp(self, i, j, color) -> None:
        """
        Updates either the red or blue connected component  
        when adding a new stone at place i,j
        """
        match color:
            case Color.Red:
                conn_comp = self.red_conn_comp
                print("selected red conn comp")
                print(f"id:{id(conn_comp)}")
            case Color.Blue:
                conn_comp = self.blue_conn_comp
                print("selected blue conn comp")
                print(f"id:{id(conn_comp)}")

        all_nbrs = self.find_neighbours((i, j))
        nbrs = set((nbr.x, nbr.y) for nbr in all_nbrs if nbr.color == color)

        for nbr in nbrs:
            conn_comp.union((i, j), nbr)

    def place_stone(self, i: int, j: int, color: Color) -> 'Board':
        """
        place a stone at cell i,j on the board if this is empty
        and recomputes the connected components dictionary
        """
        if self[i, j].is_empty:
            self[i, j] = Cell(x=i, y=j, color=color)
            # now let's update the connected components
            # TODO: implement updated conn component
            self._update_conn_comp(i, j, color)
            print(f"{color} player has placed stone on tile {(i,j)}")
        else:
            raise ValueError(
                "Cannot place stone at cell {cell}- already occupied".format_map({"cell": self[(i, j)]}))
        return self

    def _has_color_won(self, color: Color) -> bool:
        """
        Returns true iff there exist a continous path of stones of that color
        from the two of it's borders
        """
        border_1, border_2 = self.get_borders(color)
        conn_comp = self.get_conn_comp(color)
        for node_1 in border_1:
            for node_2 in border_2:
                if conn_comp.find((node_1.x, node_1.y)) == conn_comp.find((node_2.x, node_2.y)):
                    return True
        return False

    def has_cell(self, coords: tuple[int, int]) -> bool:
        """
        has_cell function checks if the square defined by
        @param coords exists in the board.
        @return True iff the cell is in the boudaries of the board
        """
        x, y = coords
        return (0 <= x < self.dim_x) and (0 <= y < self.dim_y)

    def is_border_cell(self, coords: tuple[int, int]) -> bool:
        """
        is_border_cell checks if the @param cell is found on one of the 4 borders
        of the board
        """
        x, y = coords
        return x == 0 or x == (self.dim_x - 1) or y == 0 or y == (self.dim_y - 1)

    def get_borders(self, color: Color) -> tuple[list[Cell], list[Cell]]:
        """
        Returns a tuple containing list of those positions
        (as int,int tuples) that belong to the two borders of
        a given color
        """
        match color:
            case Color.Red:
                bottom_red = [self[x, 0] for x in range(
                    self.dim_x) if self[x, 0].color == color]
                top_red = [self[x, self.dim_y-1]
                           for x in range(self.dim_x) if self[x, self.dim_y-1].color == color]
                return (bottom_red, top_red)
            case Color.Blue:
                left_blue = [self[0, y] for y in range(
                    self.dim_y) if self[0, y].color == color]
                right_blue = [self[self.dim_x-1, y]
                              for y in range(self.dim_y) if self[self.dim_x-1, y].color == color]
                return (left_blue, right_blue)
        raise ValueError(f"Not recognised color {color}")

    def get_conn_comp(self, color: Color) -> UnionFind[tuple[int, int]]:
        """
        Given a color gives the connected component for that
        color
        """
        match color:
            case Color.Red:
                return self.red_conn_comp
            case Color.Blue:
                return self.blue_conn_comp
        raise ValueError(f"Not recognised color {color}")

    def is_red_border_cell(self, coords: tuple[int, int]) -> bool:
        """   
        Returns true if we are on one of the two red borders,
        bottom and top.
        """
        x, y = coords
        return y == 0 or y == (self.dim_y - 1)

    def is_blue_border_cell(self, coords: tuple[int, int]) -> bool:
        """   
        Returns true if we are on one of the two blue borders,
        bottom and top.
        """
        x, y = coords
        return x == 0 or x == (self.dim_x - 1)

    def find_neighbours(self, coords: tuple[int, int]) -> set[Cell]:
        """
        find_neighbours function finds all neighbouring cells
        in the board to the cell defined by @param coords
        @return list of neighbouring cells
        """

        x, y = coords

        # this is a theoretical neighborood in the
        # sense that some of this cell might be out of the board
        theoretical_nbrd = set((
            Cell(x+1, y),
            Cell(x-1, y),
            Cell(x, y+1),
            Cell(x+1, y+1),
            Cell(x-1, y-1),
            Cell(x, y-1))
        )

        nbrd = {self[cell.x, cell.y] for cell in theoretical_nbrd if self.has_cell(
            (cell.x, cell.y))}
        return nbrd

    @property
    def red_conn_comp(self) -> UnionFind[tuple[int, int]]:
        return self._red_conn_comp

    @property
    def blue_conn_comp(self) -> UnionFind[tuple[int, int]]:
        return self._blue_conn_comp

    @property
    def empty_positions(self) -> list[tuple[int, int]]:
        """
        Returns all the positions (i,j) for which the
        (i,j) cell is empty
        """
        # TODO:reimplement this with self.__iter__
        return [(x, y) for y, row in enumerate(self._board) for x, _ in enumerate(row) if self[x, y].is_empty]


if __name__ == "__main__":
    # TODO when happy these all work move to the test file
    dim_x = 11
    dim_y = 11
    nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
    uf_red = UnionFind(nodes)
    uf_blue = UnionFind(nodes)
    board = Board(dim_x=dim_x, dim_y=dim_y,
                  red_conn_comp=uf_red, blue_conn_comp=uf_blue)

    print("STARTING BOARD: ")
    print(str(board))
    cell_2_3 = Cell(2, 3, Color.Red)
    board.__setitem__((2, 3), cell_2_3)
    print("CHANGED BOARD: ")

    print(str(board))
    print(len(board.empty_positions))

    # now try placing stone

    board.place_stone(3, 3, Color.Blue)
    print("CHANGED BOARD AFTER PLACING: ")
    print(str(board))

    print(len(board.empty_positions))

    assert board.has_cell((4, 1))

    assert not board.is_border_cell((4, 1))

    assert board.is_border_cell((10, 1))

    print(str(board))

    print(f"The len of blue conn comp:{len(board.blue_conn_comp)}")
    print(f"The len of red conn comp:{len(board.red_conn_comp)}")

    board.place_stone(4, 3, Color.Blue)
    print("CHANGED BOARD AFTER PLACING: ")
    print(str(board))
    print(f"The len of blue conn comp:{len(board.blue_conn_comp)}")
    print(f"The len of red conn comp:{len(board.red_conn_comp)}")
