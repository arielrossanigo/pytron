import random

from pytron.bot import Bot, Action


class PlayerBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick = 0
        self.counter = 0

    def get_action(self, board):
        if self.tick == self.counter:
            action = Action.Rigth
            self.counter = 0
            self.tick += 1
        else:
            action = Action.Forward
            self.counter += 1

        return action
