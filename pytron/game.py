import copy
import importlib
import json
import random
from collections import defaultdict
from itertools import zip_longest

from pytron.bot import Orientation

POSSIBLE_DELTAS = {
                    #   x   y
                    #  col row
    Orientation.North: (0, -1),
    Orientation.East:  (1,  0),
    Orientation.South: (0,  1),
    Orientation.West: (-1,  0),
}


class GameState:
    def __init__(self, bots, n_rows, n_columns):
        self.bots_path = []
        self.bots_orientation = []
        self.used_positions = set()
        for _ in bots:
            while True:
                row_number = random.randint(1, n_rows - 1)
                col_number = random.randint(1, n_columns - 1)
                position = (col_number, row_number)
                if position not in self.used_positions:
                    break
            self.bots_path.append([position])
            self.used_positions.add(position)
            self.bots_orientation.append(random.choice(list(Orientation)))

    def get_bot_current_position(self, bot_id):
        return self.bots_path[bot_id][-1]

    def get_bot_orientation(self, bot_id):
        return self.bots_orientation[bot_id]

    def get_bot_path(self, bot_id):
        return self.bots_path[bot_id]

    def append_position_to_bot(self, bot_id, position):
        self.bots_path[bot_id].append(position)
        self.used_positions.add(position)

    def set_bot_orientation(self, bot_id, orientation):
        self.bots_orientation[bot_id] = orientation

    def __str__(self):
        lines = [' '.join(str(x) for x in path) + f' # {orientation} '
                 for path, orientation in zip(self.bots_path, self.bots_orientation)]
        return '\n'.join(lines)


class PytronEngine:
    def __init__(self, bots, n_rows=10, n_columns=10):
        self.bots = bots
        self.dead_bots = set()
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.state = GameState(bots, n_rows, n_columns)
        self.scores = None

    def play(self):
        while not self.game_finished():
            next_bot_status = []  # status is <position, orientation>
            current_state = copy.deepcopy(self.state)
            for bot_id, bot in enumerate(self.bots):
                bot_position = self.state.get_bot_current_position(bot_id)
                bot_orientation = self.state.get_bot_orientation(bot_id)
                if bot_id in self.dead_bots:
                    next_status = (bot_position, bot_orientation)
                else:
                    action = bot.get_action(current_state)
                    next_status = self.get_next_position_and_orientation(action, bot_id)
                next_bot_status.append(next_status)

            self.update_state(next_bot_status)

        # scores are the number of steps the bot survive
        self.scores = [len(set(path)) for path in self.state.bots_path]

    def game_finished(self):
        return len(self.bots) == len(self.dead_bots)

    def update_state(self, next_position_and_orientation):
        by_position = defaultdict(list)

        for bot_id, (position, _) in enumerate(next_position_and_orientation):
            # if someone goes outside of the board, it lose
            row, col = position
            if not 0 <= row <= self.n_rows or not 0 <= col <= self.n_columns:
                self.dead_bots.add(bot_id)

            # if someone crash some tail, it lose
            if position in self.state.used_positions:
                self.dead_bots.add(bot_id)

            # if 2 or more bots goes to the same place, all lose
            by_position[position].append(bot_id)

        # if 2 or more bots goes to the same place, all lose
        for position, bots in by_position.items():
            if len(bots) > 1:
                self.dead_bots = self.dead_bots.union(set(bots))

        for bot_id, (position, orientation) in enumerate(next_position_and_orientation):
            # add the head of the pytron
            self.state.append_position_to_bot(bot_id, position)
            self.state.set_bot_orientation(bot_id, orientation)

    def get_next_position_and_orientation(self, action, bot_id):
        current_row, current_column = self.state.get_bot_current_position(bot_id)
        current_orientation = self.state.get_bot_orientation(bot_id)

        next_orientation_in_degrees = current_orientation.value + action.value
        # ensure values between 0 and 270
        next_orientation = Orientation((next_orientation_in_degrees + 360) % 360)

        delta_row, delta_col = POSSIBLE_DELTAS[next_orientation]
        next_position = current_row + delta_row, current_column + delta_col
        return next_position, next_orientation

    def get_bots_historical_positions(self):
        return self.state.bots_path


def load_bot(bot_id, bot_name, size):
    module = importlib.import_module(f'pytron.bots.{bot_name}.main')
    bot = module.PlayerBot(bot_id, bot_name, size, size)
    return bot


class Match:
    'Class to keep bots, engine and scores'
    def __init__(self, bots_names, size):
        self.bots_names = bots_names
        self.size = size
        self.bots = [load_bot(bot_id, bot, size) for bot_id, bot in enumerate(bots_names)]
        self.engine = PytronEngine(self.bots, size, size)

    def play(self):
        self.engine.play()

    def save(self, filename):
        if not self.engine.game_finished():
            raise Exception("Play the match first")

        steps = []
        for players_positions in zip_longest(*self.engine.get_bots_historical_positions()):
            steps.append(players_positions)

        by_bot = [(bot_id, self.bots[bot_id].name, score)
                  for bot_id, score in enumerate(self.engine.scores)]
        score_board = sorted(by_bot, key=lambda x: x[-1], reverse=True)

        result = {
            'size': self.size,
            'steps': steps,  # step, players, positions
            'score_board': score_board
        }
        with open(filename, 'wt', encoding='utf-8') as f:
            json.dump(result, f)
