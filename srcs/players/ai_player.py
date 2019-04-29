import random
from srcs.players.player import Player


class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
        print("create AI")

    def move(self):
        x = random.randrange(0, self.board.size)
        y = random.randrange(0, self.board.size)
        if self.board.is_allowed(x, y, self.stone):
            self.board.put_stone(x, y, self.stone)