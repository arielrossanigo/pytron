import random

from bot import Bot, Action


class PlayerBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick = 0
        self.turns = 1

    def get_action(self, board):
        if self.tick % self.turns == 0:
            action = Action.Forward
            self.turns += 1
        else:
            action = Action.Rigth
        self.tick += 1
        return action
