import random


class Player(object):
    board = None  # the board object
    stone = None  # the stone -> STONE_BLACK, STONE_WHITE (defined in srcs.const)

    def __init__(self, board, stone):
        self.board = board
        self.stone = stone

    def move(self):
        raise NotImplementedError("implement this function in the subclass")

    def has_win(self):
        print("[WARNING]: has_win function to do")
        win = random.randrange(0, 11)
        if win == 10:
            return True
        return False