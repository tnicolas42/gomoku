import time
from srcs.players.player import Player


class RealPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)

    def move(self):
        self.is_clicked_on = False
        is_moving = False
        while not is_moving:
            time.sleep(0.05)
            self.game.gui.update()
            if self.is_clicked_on:
                if self.game.board.is_allowed(*self.clicked_pos, self.stone):
                    self.game.board.put_stone(*self.clicked_pos, self.stone)
                    is_moving = True
                self.is_clicked_on = False
        self.game.gui.update()
