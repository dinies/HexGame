import random
from hexgame.src.color import Color
from hexgame.src.board import Board

__author__ = "Gianpiero Cea"


class Player:
    """ player.py A player of a hex game, either red or blue"""

    def __init__(self, color=Color.Red):
        self.color: self.Color = color

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        return self.color == other.color

    def _place_stone(self, board: Board, i, j) -> Board:
        new_board = board.place_stone(i, j, self.color)
        return new_board

    # here we define the playing logic
    def play(self, board: Board) -> Board:
        # TODO: Implements other logic:AI/Human etc
        # !!!RANDOM POLICY
        next_move: tuple[int, int] = random.choice(list(board.empty_positions))
        i, j = next_move
        new_board = self._place_stone(board, i, j)
        return new_board


if __name__ == "__main__":
    # TODO: implements proper tests usng pytest
    player = Player()
    print(player.color)
