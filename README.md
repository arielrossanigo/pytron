# pytron

Tron game for python bots.


## Installation

- Clone this repo
- Install it in a virtual env with `pip install -e .`


## Try out pytron

You can run a game using some defaults bot, with the following command:

```bash
pytron dumb_bot spiral
```

This will run a game with only two players: `dumb_bot` (which will make random
movements) and `spiral` (which will make a spiral movement)

The winner will be the bot that can make the longest movement without hit itself,
other bot, or a border.

After running the game, you can visualize the match in a browser. Try it out!


## Create your own bot!

### Custom bot snippet

To create a new bot, create a module in `/pytron/bots/<your_bot_name>/main.py`, and
define a PlayerBot class, as follows:


```python
import random

from pytron.bot import Bot, Action


class PlayerBot(Bot):
    def get_action(self, board):
        return Action.Right

```
In `get_action` you can define the logic for your bot. That method will be called in
each iteration of the game. For example, in the previous example, the bot
will turn right in each iteration. The possible actions are `Right`, `Left` and
`Forward`.


### Play pytron with your new bot

To test how good is your new bot, just play pytron selecting it as a new player.

You can let your bot challange one of our bots:
```bash
pytron <your_bot_name> spiral
```

Also, you can add multiple instances of the same bot:

```bash
pytron <your_bot_name> <your_bot_name> spiral escalerita escalerita
```

### Board param

To create a smarter bot, you may need to know the current state of the game. You can
know everything you need about the state with the param `board`.

`board` is an instance of `GameState`, and have the following attributes:

- `bots_path`: a list of all the positions for each bot, in each iteration. For example,
if a bot starts in position (1, 1), and moves to (1, 2), and another bot starts in
(3, 2) and moves to (2, 2), the current state of `bots_path` is:
```python
[
#    1st it,  2nd it
    [(1, 1), (1 2)],  # first bot
    [(3, 2), (2 2)],  # second bot
]
```
The positions are read as (column_number, row_number).

- `bots_orientation`: the orientation of each bot, which means it will be the direction
where it will move if the returend action is `Forward`. The possible values are
`Orientation.North`, `Orientation.East`, `Orientation.South` and `Orientation.West`.

- `used_positions`: A list with all the already occupied positions.


### Info in Bot instance

You can also found some important info in the bot instance (`self` inside the
`get_action` method.)

- `id`: id of the bot, which is also its index in `board.bots_path` and
`board.bots_orientation`. Following the previous example if `self.id == 0` that means
`self` is the bot that started in the position (1, 1) and now is currently in (1, 2).

- `name`: the name of your bot (from the folder that contains the `main.py` file)

- `board_row_size`: the number of rows in the board. For example, if
`board_row_size == 10`, the last valid row index is `9`, and if your bot goes to (10, 0) it
will loose).

- `board_column_size`: the number of columns in the board.
