"""board.py: A board to play a game of hex on"""
from hexgame.src.cell import Cell
from hexgame.src.color import Color

BOARD_DEFAULT_X_DIM = BOARD_DEFAULT_Y_DIM = int(11)

__author__ = "Gianpiero Cea"

"""
 A board is a set of exagonal cells stacked in a 2D matrix shape.
 It can be indexed similarly to a matrix with (x, y) coordinates.
 The (0,0) coordinate starts at the bottom left corner of the board.
 The x coordinate indexes horizontally (going from left to right)
 and the y vertically (going from bottom to top)
 The exagonal cells make so that the board is slanted in a
 romboidal shape. The slanting goes to the left.
 ----------
 '         '
  '         '
   '         '
     ----------
"""


class Board:

    def __init__(self,
                 dim_x: int = BOARD_DEFAULT_X_DIM,
                 dim_y: int = BOARD_DEFAULT_Y_DIM):
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
                "Cannot place stone at cell {cell}- already"
                "occupied".format_map({"cell": self[(i, j)]}))

    """
    has_cell function checks if the square defined by
    @param coords exists in the board.
    @return True iff the cell is in the boudaries of the board
    """

    def has_cell(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        return (0 <= x < self.dim_x) and (0 <= y < self.dim_y)

    """
    is_border_cell checks if the @param cell is found on one of the 4 borders
    of the board
    """

    def is_border_cell(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        return (x == 0 or x == (self.dim_x - 1) or
                y == 0 or y == (self.dim_y - 1))

    """
    find_neighbours function finds all neighbouring cells
    in the board to the cell defined by @param coords
    @return list of neighbouring cells
    """

    def find_neighbours(self, coords: tuple[int, int]) -> set[Cell]:
        # TODO: finish this
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

        nbrd = {cell for cell in theoretical_nbrd if self.has_cell(
            (cell.x, cell.y))}
        return nbrd

    def __repr__(self) -> str:
        pass


if __name__ == "__main__":
    # TODO when happy these all work move to the test file
    board = Board()

    print("STARTING BOARD: ")
    print(board._board)
    cell_2_3 = Cell(2, 3, Color.Red)
    board.__setitem__((2, 3), cell_2_3)
    print("CHANGED BOARD: ")

    print(board._board)

    # now try placing stone

    board.place_stone(3, 3, Color.Blue)
    print("CHANGED BOARD AFTER PLACING: ")
    print(board._board)

    assert board.has_cell(Cell(4, 1, None))
    assert not board.is_border_cell(Cell(4, 1, None))
    assert board.is_border_cell(Cell(10, 1, None))
