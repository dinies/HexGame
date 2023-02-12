"""board.py: A board to play a game of hex on"""

__author__      = "Gianpiero Cea"



from hexgame.src.cell import Cell
from hexgame.src.color import Color

BOARD_DEFAULT_X_DIM = BOARD_DEFAULT_Y_DIM = int(11)

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

    def __init__(self, dim_x : int = BOARD_DEFAULT_X_DIM , dim_y : int= BOARD_DEFAULT_Y_DIM ):
        self.dim_x :int = dim_x
        self.dim_y :int = dim_y

        self._board :list[list[Cell]] = self._make_board(dim_x,dim_y) 
        self._connected_components : dict[Color,set[set[Cell]]] = {Color.Blue :{}, Color.Red:{}}

    
    def __getitem__(self, coord : tuple):
        x, y = coord
        return self._board[x][y]
    
    def __setitem__(self, coord : tuple, val : Cell):
        x, y = coord
        #TODO: I am not liking this..check later if we should drop x,y in cell
        assert val.x == x
        assert val.y == y
        self._board[x][y] = val


    def _make_board(self,dim_x :int,dim_y:int) -> list[list[Cell]]:
        """
        represents a dim_x * dim_y board of hexagonal cells
        """
        return [[Cell(x,y) for y in range(dim_y) ] for x in range(dim_x) ]
    
    def place_stone(self, i:int, j:int, color : Color) -> 'Board':
        """
        place a stone at cell i,j on the board 
        and recomputes the connected components dictionary
        """
        new_board = self._board
        new_board[i]

    """
    has_cell function checks if the square defined by
    @param coords exists in the board.
    @return True iff the cell is in the boudaries of the board
    """

    def has_cell(self, coords: tuple[int, int]) -> bool:
        return False

    """
    find_neighbours function finds all neighbouring cells
    in the board to the cell defined by @param coords
    @return list of neighbouring cells
    """

    def find_neighbours(self, coords: tuple[int, int]) -> set[Cell]:
        return []


if __name__ == "__main__":
    board = Board()
  
    print("STARTING BOARD: ")
    print(board._board)
    cell_2_3 = Cell(2,3,Color.Red)
    board.__setitem__((2,3),cell_2_3)
    print("CHANGED BOARD: ")
    
    print(board._board)











    




