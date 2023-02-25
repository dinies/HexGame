""" game.py  a game of hex"""

from hexgame.src.color import Color
from hexgame.src.board import Board
from hexgame.src.player import Player
from logging import Logger
import enum
__author__ = "Gianpiero Cea"


class Game:
    class GameStatus(enum.Enum):
        Finished = 0
        Running = 1

    def __init__(self):
        self.player_1: Player = Player()
        self.player_2: Player = Player(Color.Blue)
        self.board: Board = Board()
        self.status: self.GameStatus = self.GameStatus.Running
        self.move: int = 0
        self.current_player: Player = self.player_1

    def _play(self):
        # player  move
        new_board = self.current_player.play(self.board)
        self.board = new_board

        if self._has_player_won():
            self.status = self.GameStatus.Finished

        self.move += 1
        self.current_player = self._next_player()

    def _next_player(self):
        return self.player_1 if self.current_player == self.player_2 else self.player_2

    def _has_player_won(self):
        # TODO: change this to actual logic!!
        if self.move == 10:
            return True
        return False

    def start(self):
        while self.status == self.GameStatus.Running:
            print(self.board)
            # TODO:remove this debug logging
            print('blue: ', self.board.blue_graph)
            print('red: ', self.board.red_graph)

            self._play()
        else:
            # TODO:move this to a logger/cli
            print(str(self.current_player.color)+' wins')


if __name__ == "__main__":
    game = Game()
    game.start()
