from src.color import Color
from src.board import Board

__author__      = "Gianpiero Cea"

class Player:
    """ player.py A player of a hex game, either red or blue"""


    def __init__(self,color= Color.Red):
        self.color : self.Color = color

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        return self.color == other.color


    def _place_stone(board :Board,i,j) ->  Board:
        new_board = board.place_stone(i,j)
        return new_board 

    #here we define the playing logic
    def play(self,board: Board) -> Board:
        #TODO: implement a random policy
        pass




if __name__ == "__main__":
    #TODO: implements proper tests usng pytest
    player = Player()
    print(player.color)









