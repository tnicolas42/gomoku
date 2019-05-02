import time
from srcs.players.player import Player


class RealPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)

    def move(self):
        """
        this function is called when the AI need to move
        -> put a stone on the board after clicked
        """
        self.is_clicked_on = False
        is_moving = False
        while not is_moving:
            time.sleep(0.05)
            if self.is_clicked_on:
                if self.game.board.is_allowed(*self.clicked_pos, self.stone):
                    self.game.board.put_stone(*self.clicked_pos, self.stone)
                    is_moving = True
                self.is_clicked_on = False