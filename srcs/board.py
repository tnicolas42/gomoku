from srcs.const import *


class Board(object):
    game = None  # the game object
    content = []  # this is the board
    size = None
    remain_places = None  # number of remaining places

    def __init__(self, game, size=19):
        self.game = game
        self.content = [[STONE_EMPTY for i in range(size)] for j in range(size)]
        self.size = size
        self.remain_places = size * size

    def put_stone(self, x, y, stone):
        if x >= self.size or y >= self.size:
            print("[ERROR]: unable to put a stone at %d %d -> out of board" % (x, y))
            exit(1)
        self.content[y][x] = stone
        self.remain_places -= 1

        # try to destroy stones

        # this is the condition to know if we can destroy some stones
        # x1y1 and x2y2 are the coordinate of potentials destroyed stones
        # x3y3 is the oposite stone
        destroy_cond = lambda x1, y1, x2, y2, x3, y3: (
                        0 <= x1 < self.size and 0 <= x2 < self.size and 0 <= x3 < self.size and
                        0 <= y1 < self.size and 0 <= y2 < self.size and 0 <= y3 < self.size and
                        self.content[y3][x3] == stone and
                        self.content[y2][x2] == self.content[y1][x1] and
                        self.content[y1][x1] not in (STONE_EMPTY, stone))
        # this tab contains all configuration to destroy stones
        destroy_tab = (
            (x, y-1, x, y-2, x, y-3),
            (x, y+1, x, y+2, x, y+3),
            (x-1, y, x-2, y, x-3, y),
            (x+1, y, x+2, y, x+3, y),
            (x+1, y+1, x+2, y+2, x+3, y+3),
            (x+1, y-1, x+2, y-2, x+3, y-3),
            (x-1, y+1, x-2, y+2, x-3, y+3),
            (x-1, y-1, x-2, y-2, x-3, y-3),
        )
        for destroy_tab_i in destroy_tab:
            if destroy_cond(*destroy_tab_i):
                self.content[destroy_tab_i[1]][destroy_tab_i[0]] = STONE_EMPTY
                self.content[destroy_tab_i[3]][destroy_tab_i[2]] = STONE_EMPTY
                self.game.players[stone].destroyed_stones_count += 2
                self.remain_places += 2

        # check aligned stones
        max_align = 0
        # align in x
        nb_aligned = 1
        new_x = x - 1
        new_y = y
        while new_x >= 0:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x -= 1
        new_x = x + 1
        while new_x < self.size:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x += 1
        max_align = max(max_align, nb_aligned)

        # align in y
        nb_aligned = 1
        new_x = x
        new_y = y - 1
        while new_y >= 0:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_y -= 1
        new_y = y + 1
        while new_y < self.size:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_y += 1
        max_align = max(max_align, nb_aligned)

        # align in diagonal 1
        nb_aligned = 1
        new_x = x - 1
        new_y = y - 1
        while new_x >= 0 and new_y >= 0:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x -= 1
            new_y -= 1
        new_x = x + 1
        new_y = y + 1
        while new_x < self.size and new_y < self.size:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x += 1
            new_y += 1
        max_align = max(max_align, nb_aligned)

        # align in diagonal 2
        nb_aligned = 1
        new_x = x - 1
        new_y = y + 1
        while new_x >= 0 and new_y < self.size:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x -= 1
            new_y += 1
        new_x = x + 1
        new_y = y - 1
        while new_x < self.size and new_y >= 0:
            if self.content[new_y][new_x] == stone:
                nb_aligned += 1
            else:
                break
            new_x += 1
            new_y -= 1
        max_align = max(max_align, nb_aligned)

        if max_align >= NB_ALIGNED_VICTORY:
            print("[WARNING]: has_win function to finish -> check 5 aligned stones without possibility of desrtoy one")
            self.game.players[stone].is_win_aligned = True

    def is_allowed(self, x, y, stone):
        print("[WARNING]: is_allowed function to finish")
        if self.content[y][x] is not STONE_EMPTY:
            return False
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
                color = [c.EOC, c.EOC]
                txt = ' . '
                if self.content[y][x] == STONE_EMPTY:
                    pass
                elif self.content[y][x] == 0:
                   color = [c.WHITE, c.F_WHITE]
                elif self.content[y][x] == 1:
                    color = [c.BLACK, c.F_BLACK]
                elif self.content[y][x] == 2:
                    color = [c.RED, c.F_RED]
                elif self.content[y][x] == 3:
                    color = [c.GREEN, c.F_GREEN]
                elif self.content[y][x] == 4:
                    color = [c.BLUE, c.F_BLUE]
                elif self.content[y][x] == 5:
                    color = [c.YELLOW, c.F_YELLOW]
                elif self.content[y][x] == 6:
                    color = [c.MAGENTA, c.F_MAGENTA]
                elif self.content[y][x] == 7:
                    color = [c.CYAN, c.F_CYAN]
                else:
                    txt = '%2d ' % (self.content[y][x])
                print(end=color[0] + color[1] + txt + c.EOC)
            print('|')
        for i in range(self.size):
            if i == 0:
                print(end='*')
            print(end='---')
        if i == self.size - 1:
            print('*')
