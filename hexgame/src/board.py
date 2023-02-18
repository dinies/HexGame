"""board.py: A board to play a game of hex on"""
from hexgame.src.cell import Cell
from hexgame.src.color import Color
from collections.abc import Iterator

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

    def __init__(self, dim_x: int = BOARD_DEFAULT_X_DIM, dim_y: int = BOARD_DEFAULT_Y_DIM) -> 'Board':
        self.dim_x: int = dim_x
        self.dim_y: int = dim_y

        self._board: list[list[Cell]] = self._make_board(dim_x, dim_y)
        self._connected_components: dict[Color, set[set[Cell]]] = {
            Color.Blue: {}, Color.Red: {}}

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

    def place_stone(self, i: int, j: int, color: Color) -> 'Board':
        """
        place a stone at cell i,j on the board if this is empty
        and recomputes the connected components dictionary
        """
        if self[i, j].is_empty:
            self[i, j] = Cell(x=i, y=j, color=color)
        else:
            raise ValueError(
                "Cannot place stone at cell {cell}- already occupied".format_map({"cell": self[(i, j)]}))

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

    def find_neighbours(self, coords: tuple[int, int]) -> set[Cell]:
        """
        find_neighbours function finds all neighbouring cells
        in the board to the cell defined by @param coords
        @return list of neighbouring cells
        """

        x, y = coords
        nbrs = set()

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

        nbrd = {cell for cell in theoretical_nbrd if self.has_cell(
            (cell.x, cell.y))}
        return nbrd

    @property
    def empty_positions(self) -> Iterator[tuple[int, int]]:
        """
        Returns all the positions (i,j) for which the
        (i,j) cell is empty
        """
        # TODO:reimplement this with self.__iter__
        return ((x, y) for y, row in enumerate(self._board) for x, _ in enumerate(row) if self[x, y].is_empty)


if __name__ == "__main__":
    # TODO when happy these all work move to the test file
    board = Board()

    print("STARTING BOARD: ")
    print(board._board)
    cell_2_3 = Cell(2, 3, Color.Red)
    board.__setitem__((2, 3), cell_2_3)
    print("CHANGED BOARD: ")

    print(board._board)
    print(len(list(board.empty_positions)))

    # now try placing stone

    board.place_stone(3, 3, Color.Blue)
    print("CHANGED BOARD AFTER PLACING: ")
    print(board._board)

    print(len(list(board.empty_positions)))

    assert board.has_cell((4, 1))

    assert not board.is_border_cell((4, 1))

    assert board.is_border_cell((10, 1))

    print(repr(board))

    print(str(board))
