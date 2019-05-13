import time
import random
from srcs.const import *


class Player(object):
    """
    this is the parent object of all players types (REAL, AI)
    there is one Player object foreach players
    """
    game = None  # the game object
    stone = None  # the stone -> int from 0 to n
    destroyed_stones_count = 0  # number of destroyed stones
    is_win_aligned = False  # == True if the player win because of 5 or more stones aligned (calculate on board.py)
    nb_stone = 0  # == the number of stones on the board

    is_clicked_on = False
    clicked_pos = [0, 0]
    time_last_move = 0.0

    def __init__(self, game, stone):
        self.game = game
        self.stone = stone

    def moving(self):
        before = time.time()
        ret = self.move()
        self.time_last_move = time.time() - before
        return ret

    def move(self):
        """
        this function is called when the player need to move
        """
        raise NotImplementedError("implement this function in the subclass")

    def clicked_on(self, x, y):
        """
        when the player click on the board, if this function is called (called only on the actual player)
        """
        self.is_clicked_on = True  # say that the player has clicked (set to false in move function)
        self.clicked_pos = [x, y]  # the position of the click

    def has_win(self):
        """
        this function if called after move
        return True if the player win
        """
        if self.is_win_aligned:
            print("win with %d or more stones aligned" % (G.NB_ALIGNED_VICTORY))
            return True

        if self.destroyed_stones_count >= G.STONES_DESTROYED_VICTORY:
            print("win because %d stones destroyed" % (self.destroyed_stones_count))
            return True

        return False