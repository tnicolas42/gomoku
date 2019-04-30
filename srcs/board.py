from srcs.const import *


class Board(object):
    content = []  # this is the board
    size = None

    def __init__(self, size=19):
        self.content = [[STONE_EMPTY for i in range(size)] for j in range(size)]
        self.size = size

    def put_stone(self, x, y, stone):
        if x >= self.size or y >= self.size:
            print("[ERROR]: unable to put a stone at %d %d -> out of board" % (x, y))
            exit(1)
        self.content[y][x] = stone

    def is_allowed(self, x, y, stone):
        print("[WARNING]: is_allowed function to finish")
        return True

    def print_board(self):
        for i in range(self.size):
            if i == 0:
                print(end='*')
            print(end='---')
        if i == self.size - 1:
            print('*')
        for y in range(self.size):
            print(end='|')
            for x in range(self.size):
                if self.content[y][x] == STONE_EMPTY:
                    print(end=' . ')
                elif self.content[y][x] == 0:
                    print(end=c.WHITE + c.F_WHITE + '   ' + c.EOC)
                elif self.content[y][x] == 1:
                    print(end=c.BLUE + c.F_BLUE + '   ' + c.EOC)
                else:
                    print(end='%2d ' % (self.content[y][x]))
            print('|')
        for i in range(self.size):
            if i == 0:
                print(end='*')
            print(end='---')
        if i == self.size - 1:
            print('*')
