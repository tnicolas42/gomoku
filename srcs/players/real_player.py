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
        while not is_moving and not self.game.quit and not self.game.reset_game:
            time.sleep(0.05)
            if self.is_clicked_on:
                self.game.gui.gui_game.error_pos[0] = [None, None]  # reset the error stone
                if self.game.board.is_allowed(*self.clicked_pos, self.stone):
                    self.game.board.put_stone(*self.clicked_pos, self.stone)
                    is_moving = True
                else:
                    self.game.gui.gui_game.error_pos = [self.clicked_pos, time.time()]  # the position is not available -> disable it
                self.is_clicked_on = False