""" cell.py: A single hexagonal cell that makes up a hex board """
from hexgame.color import Color

__author__ = "Gianpiero Cea"


class Cell:
    __match_args__ = ("x", "y", "color")

    def __init__(self, x: int, y: int, color: Color = Color.Empty):
        self._is_empty: bool = color == Color.Empty
        self.color: Color = color
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return "({x},{y})- Color:{color}".format_map({"x": self.x, "y": self.y,
                                                      "color": self.color})

    def __str__(self) -> str:
        # TODO: str is for pretty display-can make repr more dev like?
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: 'Cell') -> bool:
        return self.x == __o.x and self.y == __o.y and self.color == __o.color

    @property
    def is_empty(self) -> bool:
        return self._is_empty
