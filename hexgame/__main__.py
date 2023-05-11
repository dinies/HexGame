from hexgame.color import Color
from hexgame.board import Board
from hexgame.player import Player
from hexgame.unionfind import UnionFind
from hexgame.game import Game

if __name__ == "__main__":
    dim_x = 5
    dim_y = 5
    nodes = [(x, y) for y in range(dim_y) for x in range(dim_x)]
    uf_red = UnionFind(nodes)
    uf_blue = UnionFind(nodes)
    board = Board(
        dim_x=dim_x, dim_y=dim_y, red_conn_comp=uf_red, blue_conn_comp=uf_blue
    )
    player_1 = Player(mode=Player.PlayerMode.Keyboard)
    player_2 = Player(color=Color.Blue, mode=Player.PlayerMode.Keyboard)
    game = Game(board=board, player_1=player_1, player_2=player_2)
    game.start()
