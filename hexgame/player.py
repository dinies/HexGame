import random
import enum
import re
from hexgame.color import Color
from hexgame.board import Board

__author__ = "Gianpiero Cea"


class Player:
    """player.py A player of a hex game, either red or blue"""

    class PlayerMode(enum.Enum):
        AI = 0
        Keyboard = 1

    def __init__(self, color: Color = Color.Red, mode: PlayerMode = PlayerMode.AI):
        self.color: Color = color
        self.mode = mode

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        return self.color == other.color

    def _place_stone(self, board: Board, i, j):
        board.place_stone(i, j, self.color)

    # here we define the playing logic
    def play(self, board: Board):
        """
        The main method that defines the playing behaviour
        based on player mode
        """
        match self.mode:
            case self.PlayerMode.AI:
                self._random_policy(board)
            case self.PlayerMode.Keyboard:
                self._get_keyboard_move(board)
            case _:
                raise ValueError(f"Unknown mode {self.mode}")

    def _random_policy(self, board: Board):
        """
        Implements a random policy
        """
        available_actions = board.possible_moves
        if (available_actions) != []:
            next_move: tuple[int, int] = random.choice(available_actions)
            i, j = next_move
            self._place_stone(board, i, j)

    def _get_keyboard_move(self, board: Board):
        """
        Waits for the keyboard input to get
        a move
        """
        available_actions = board.possible_moves
        if (available_actions) != []:
            valid_coords = False
            while not valid_coords:
                print(
                    f"Please insert the coords where to place stone \
                    for player {self.color}"
                )
                print("Pass x coord:")
                inp = input()
                if re.match("^[0-9]*$", inp) and len(inp) > 0:
                    i = int(inp)
                    print("Pass y coord:")
                    inp = input()
                    if re.match("^[0-9]*$", inp) and len(inp) > 0:
                        j = int(inp)
                        try:
                            valid_coords = (
                                board.has_cell((i, j)) and (i, j) in available_actions
                            )
                            self._place_stone(board, i, j)
                        except ValueError as e:
                            print(e)


if __name__ == "__main__":
    # TODO: implements proper tests usng pytest
    player = Player()
    print(player.color)
