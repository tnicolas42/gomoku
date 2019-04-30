import time
from srcs.players.player import Player


class RealPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)
        print("create real player")

    def move(self):
        self.is_clicked_on = False
        is_moving = False
        while not is_moving:
            self.game.gui.update()
            if self.is_clicked_on:
                print("clicked")
                if self.game.board.is_allowed(*self.clicked_pos, self.stone):
                    self.game.board.put_stone(*self.clicked_pos, self.stone)
                    is_moving = True
                self.is_clicked_on = False
            time.sleep(0.1)
        self.game.gui.update()
