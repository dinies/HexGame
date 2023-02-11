""" cell.py: A single hexagonal cell that makes up a hex board """
from hexgame.src.color import Color

__author__      = "Gianpiero Cea"

class Cell:
    def __init__(self,x :int,y:int,color : Color = None):
        self._is_empty :bool = True
        self.color : Color = color
        self.x : int = x
        self.y : int = y

    def __repr__(self) -> str:
        return "({x},{y})- Color:{color}".format_map({"x":self.x,"y":self.y,"color":self.color})

    @property
    def is_empty(self) -> bool:
        return self._is_empty




