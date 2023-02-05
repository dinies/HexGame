"""board.py: A board to play a game of hex on"""

__author__      = "Gianpiero Cea"



from cell import Cell
from color import Color

BOARD_DEFAULT_X_DIM = BOARD_DEFAULT_Y_DIM = int(11)


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
        return [[Cell(x,y) for x in range(dim_x) ] for y in range(dim_y) ]
    
    def place_stone(self, i:int, j:int, color : Color) -> 'Board':
        """
        place a stone at cell i,j on the board 
        and recomputes the connected components dictionary
        """
        new_board = self._board
        new_board[i]



if __name__ == "__main__":
    board = Board()
  
    print("STARTING BOARD: ")
    print(board._board)
    cell_2_3 = Cell(2,3,Color.Red)
    board.__setitem__((2,3),cell_2_3)
    print("CHANGED BOARD: ")
    
    print(board._board)











    




