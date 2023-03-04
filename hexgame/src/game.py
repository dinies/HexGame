""" game.py  a game of hex"""

from hexgame.src.color import Color
from hexgame.src.board import Board
from hexgame.src.player import Player
from hexgame.src.unionfind import UnionFind
from logging import Logger
import enum
__author__ = "Gianpiero Cea"


class Game:
    class GameStatus(enum.Enum):
        Finished = 0
        Running = 1

    def __init__(self,
                 board: Board, player_1: Player = Player(),
                 player_2: Player = Player(Color.Blue)):
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        self.board: Board = board
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
        if self.move > 60:
            return True
        return False

    def start(self):
        while self.status == self.GameStatus.Running:
            print(self.board)
            # TODO:remove this debug logging
            print(f'blue conn comp len: {len( self.board.blue_conn_comp)}')
            print(f'red conn comp len: { len(self.board.red_conn_comp)}')

            self._play()
        else:
            # TODO:move this to a logger/cli
            print(str(self.current_player.color)+' wins')


if __name__ == "__main__":

    dim_x = 5
    dim_y = 5
    nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
    uf_red = UnionFind(nodes)
    uf_blue = UnionFind(nodes)
    board = Board(dim_x=dim_x, dim_y=dim_y,
                  red_conn_comp=uf_red, blue_conn_comp=uf_blue)
    player_1 = Player()
    player_2 = Player(color=Color.Blue)
    game = Game(board=board,
                player_1=player_1,
                player_2=player_2
                )
    game.start()
