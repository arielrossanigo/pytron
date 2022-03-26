from enum import Enum


class Action(Enum):
    Left = -90
    Rigth = 90
    Forward = 0


class Orientation(Enum):
    North = 0
    East = 90
    South = 180
    West = 270


class Bot:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def get_action(self, board):
        pass

