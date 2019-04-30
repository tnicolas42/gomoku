import random


class Player(object):
    game = None  # the game object
    stone = None  # the stone -> STONE_BLACK, STONE_WHITE (defined in srcs.const)

    is_clicked_on = False
    clicked_pos = [0, 0]

    def __init__(self, game, stone):
        self.game = game
        self.stone = stone

    def move(self):
        raise NotImplementedError("implement this function in the subclass")

    def clicked_on(self, x, y):
        self.is_clicked_on = True
        self.clicked_pos = [x, y]

    def has_win(self):
        print("[WARNING]: has_win function to do")
        return False