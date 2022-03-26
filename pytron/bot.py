from enum import Enum


class Action(Enum):
    Left = -90
    Right = 90
    Forward = 0


class Orientation(Enum):
    North = 0
    East = 90
    South = 180
    West = 270


class Bot:
    def __init__(self, id_, name, board_row_size, board_column_size):
        self.id = id_
        self.name = name
        self.board_row_size = board_row_size
        self.board_column_size = board_column_size

    def get_action(self, board):
        pass

