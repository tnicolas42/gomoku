import time
import random
from srcs.players.player import Player


class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)

    def move(self):
        time.sleep(0.1)
        while 42:
            x = random.randrange(0, self.game.board.size)
            y = random.randrange(0, self.game.board.size)
            if self.game.board.is_allowed(x, y, self.stone):
                self.game.board.put_stone(x, y, self.stone)
                return