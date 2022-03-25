
class Bot:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def possible_actions(self, board):
        my_row, my_column = board[self.id][-1]
        possible_deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [(my_row + delta_row, my_column + delta_col)
                for delta_row, delta_col in possible_deltas]

    def get_action(self, board):
        pass

