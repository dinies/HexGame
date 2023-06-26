""" game.py  a game of hex"""

from hexgame.color import Color
from hexgame.board import Board
from hexgame.player import Player
import enum

__author__ = "Gianpiero Cea"


class Game:
    class GameStatus(enum.Enum):
        Finished = 0
        Running = 1

    def __init__(
        self,
        board: Board,
        player_1: Player = Player(),
        player_2: Player = Player(Color.Blue),
    ):
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.board: Board = board
        self.status: self.GameStatus = self.GameStatus.Running
        self.move: int = 0
        self.current_player: Player = self.player_1

    def _play(self) -> None:
        # player  move
        chosen_move: tuple[int, int, Color] = self.current_player.play(self.board)
        i, j, color = chosen_move
        self.place_stone(i, j, color)

        if self._has_player_won():
            self.status = self.GameStatus.Finished
        else:
            self.move += 1
            self.current_player = self._next_player()

    def _next_player(self) -> Player:
        if self.current_player == self.player_2:
            return self.player_1
        else:
            return self.player_2

    def _has_player_won(self) -> bool:
        current_color = self.current_player.color
        return self.board._has_color_won(current_color)

    def start(self) -> None:
        while self.status == self.GameStatus.Running:
            print(self.board)
            self._play()
        else:
            # TODO:move this to a logger/cli
            print(str(self.current_player.color) + " wins")
