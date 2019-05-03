from srcs.const import *
from srcs.utils.stats import get_stats, get_and_print_stats


class Board(object):
    """
    this is the game board
    it contains a matrix (content) that contains info about the board:
    -1 == empty place
    0, 1, ... == stone
    [
        [-1, -1,  0, ...]
        [ 1,  0, -1, ...]
        ...
    ]
    """
    game = None  # the game object
    content = []  # this is the board
    size = None
    remain_places = None  # number of remaining places

    def __init__(self, game, size=19):
        self.game = game
        self.content = [[{'stone': STONE_EMPTY, 'vulnerability': False, 'win': False} for i in range(size)] for j in range(size)]
        self.size = size
        self.remain_places = size * size

    def check_vulnerability(self, x, y):
        """
        check the vulnerability of one stone
        """
        stone = self.content[y][x]['stone']
        if stone == STONE_EMPTY:
            return False
        # for 4 stones: abcd with b is x y -> a=x1y1 b=xy c=x2y2 d=x3y3
        vul_cond = lambda x1, y1, x2, y2, x3, y3: (
                        0 <= x1 < self.size and 0 <= x2 < self.size and 0 <= x3 < self.size and
                        0 <= y1 < self.size and 0 <= y2 < self.size and 0 <= y3 < self.size and
                        self.content[y][x]['stone'] == self.content[y2][x2]['stone'] and
                        self.content[y1][x1]['stone'] != stone and self.content[y3][x3]['stone'] != stone and
                        self.content[y1][x1]['stone'] != self.content[y3][x3]['stone'] and
                        (self.content[y1][x1]['stone'] == STONE_EMPTY or self.content[y3][x3]['stone'] == STONE_EMPTY))
        vul_tab = (
            (x-1, y, x+1, y, x+2, y),
            (x+1, y, x-1, y, x-2, y),
            (x, y-1, x, y+1, x, y+2),
            (x, y+1, x, y-1, x, y-2),
            (x-1, y-1, x+1, y+1, x+2, y+2),
            (x-1, y+1, x+1, y-1, x+2, y-2),
            (x+1, y-1, x-1, y+1, x-2, y+2),
            (x+1, y+1, x-1, y-1, x-2, y-2),
        )
        for vul_tab_i in vul_tab:
            if vul_cond(*vul_tab_i):
                self.content[y][x]['vulnerability'] = True
                return True
        self.content[y][x]['vulnerability'] = False
        return False

    def check_destroyable(self, x, y, stone):
        """
        check if the stone at 'x' 'y' can destroy some others stone
        return the list of destroyable stones [[x1, y1], [x2, y2], ...]
        """
        ret = []
        # this is the condition to know if we can destroy some stones
        # x1y1 and x2y2 are the coordinate of potentials destroyed stones
        # x3y3 is the oposite stone
        destroy_cond = lambda x1, y1, x2, y2, x3, y3: (
                        0 <= x1 < self.size and 0 <= x2 < self.size and 0 <= x3 < self.size and
                        0 <= y1 < self.size and 0 <= y2 < self.size and 0 <= y3 < self.size and
                        self.content[y3][x3]['stone'] == stone and
                        self.content[y2][x2]['stone'] == self.content[y1][x1]['stone'] and
                        self.content[y1][x1]['stone'] not in (STONE_EMPTY, stone))
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
                ret.append([destroy_tab_i[0], destroy_tab_i[1]])
                ret.append([destroy_tab_i[2], destroy_tab_i[3]])

        return ret

    def _check_aligned_dir(self, x, y, stone, addx, addy):
        """
        check the alignement in one direction (given by addx and addy)
        """
        nb_aligned = 1
        new_x = x + addx
        new_y = y + addy
        while 0 <= new_x < self.size and 0 <= new_y < self.size:
            if self.content[new_y][new_x]['stone'] == stone and not self.content[new_y][new_x]['vulnerability']:
                nb_aligned += 1
            else:
                break
            new_x += addx
            new_y += addy
        new_x = x - addx
        new_y = y - addy
        while 0 <= new_x < self.size and 0 <= new_y < self.size:
            if self.content[new_y][new_x]['stone'] == stone and not self.content[new_y][new_x]['vulnerability']:
                nb_aligned += 1
            else:
                break
            new_x -= addx
            new_y -= addy
        if nb_aligned >= NB_ALIGNED_VICTORY:
            new_x = x + addx
            new_y = y + addy
            while 0 <= new_x < self.size and 0 <= new_y < self.size:
                if self.content[new_y][new_x]['stone'] == stone and not self.content[new_y][new_x]['vulnerability']:
                    self.content[new_y][new_x]['win'] = True
                else:
                    break
                new_x += addx
                new_y += addy
            new_x = x - addx
            new_y = y - addy
            while 0 <= new_x < self.size and 0 <= new_y < self.size:
                if self.content[new_y][new_x]['stone'] == stone and not self.content[new_y][new_x]['vulnerability']:
                    self.content[new_y][new_x]['win'] = True
                else:
                    break
                new_x -= addx
                new_y -= addy
        return nb_aligned

    def check_aligned(self, x, y):
        """
        check if there is 5 or more aligned stones
        also check vulnerability of all stones
        """
        stone = self.content[y][x]['stone']
        if stone == STONE_EMPTY or self.content[y][x]['vulnerability']:
            return
        max_align = 0

        nb_aligned = self._check_aligned_dir(x, y, stone, 1, 0)
        max_align = max(max_align, nb_aligned)
        nb_aligned = self._check_aligned_dir(x, y, stone, 0, 1)
        max_align = max(max_align, nb_aligned)
        nb_aligned = self._check_aligned_dir(x, y, stone, 1, 1)
        max_align = max(max_align, nb_aligned)
        nb_aligned = self._check_aligned_dir(x, y, stone, 1, -1)
        max_align = max(max_align, nb_aligned)
        if max_align >= NB_ALIGNED_VICTORY:
            self.game.players[stone].is_win_aligned = True

    def check_winner(self):
        for x in range(self.size):
            for y in range(self.size):
                self.check_vulnerability(x, y)

        for x in range(self.size):
            for y in range(self.size):
                self.check_aligned(x, y)

    def put_stone(self, x, y, stone):
        """
        put a stone at 'x' 'y' with id 'stone'
        this function put a stone and, if needed, destroy some stones:
        before  -> -1  0  0  1
        put     ->  1  0  0  1
        destroy ->  1 -1 -1  1

        this function can also count the number of stones aligned with the putted stone to know if the player win
        if the player win -> update player.is_win_aligned
        """
        if x >= self.size or y >= self.size:
            print("[ERROR]: unable to put a stone at %d %d -> out of board" % (x, y))
            exit(1)
        self.content[y][x]['stone'] = stone
        self.game.gui.last_pos = [x, y]  # save the pos of the last placed stone
        self.remain_places -= 1

        # destroy some stones if needed
        destroyed = self.check_destroyable(x, y, stone)
        for dest_x, dest_y in destroyed:
            self.content[dest_y][dest_x]['stone'] = STONE_EMPTY
            self.game.players[stone].destroyed_stones_count += 1
            self.remain_places += 1

        # check aif there is a winner
        self.check_winner()

    def _is_free_three_dir(self, x, y, stone, addx, addy):
        """
        check if there is a free three from 'x' 'y' in direction given by 'addx' and 'addy'
        return 1 if it's a free-three
        else return 0
        """
        # list of all free-three configurations
        # 0 == every stone is OK
        # 1 == only empty stones
        # 2 == only actual stone
        # the 5th element is the 'x' 'y' element
        free_three = (
            (0, 0, 1, 2, 2, 2, 1, 0, 0),
            (0, 0, 0, 1, 2, 2, 2, 1, 0),
            (0, 1, 2, 2, 2, 1, 0, 0, 0),
            (0, 0, 0, 1, 2, 2, 1, 2, 1),
            (1, 2, 1, 2, 2, 1, 0, 0, 0),
            (0, 0, 0, 1, 2, 1, 2, 2, 1),
            (0, 2, 2, 1, 2, 1, 0, 0, 0),
            (0, 0, 1, 2, 2, 1, 2, 1, 0),
            (0, 1, 2, 1, 2, 2, 1, 0, 0),
        )
        len_free_three = len(free_three[0])
        # get a list to compare with the free-three list
        lst = [0 for i in range(len(free_three[0]))]
        i = 0
        new_x = x - (addx * (len_free_three >> 1))
        new_y = y - (addy * (len_free_three >> 1))
        while i < len_free_three:
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                lst[i] = self.content[new_y][new_x]['stone']
            new_x += addx
            new_y += addy
            i += 1
        lst[len_free_three >> 1] = stone
        for free_elem in free_three:
            is_free_three = True
            for i in range(len_free_three):
                if free_elem[i] == 0:  # no matter
                    continue
                elif free_elem[i] == 1:  # only empty
                    if lst[i] is not STONE_EMPTY:
                        is_free_three = False
                        break
                elif free_elem[i] == 2:  # only player stone
                    if lst[i] is not stone:
                        is_free_three = False
                        break
            if is_free_three:
                return 1
        return 0


    def is_allowed(self, x, y, stone):
        """
        if we want to put a stone at 'x' 'y', this function check if it's allowed (empty place, no free-threes, ...)

        if it's ok -> return True
        else -> return False
        """
        if self.content[y][x]['stone'] is not STONE_EMPTY:
            return False

        # check double three
        # if the stone destroy others stones -> no double three effect
        if len(self.check_destroyable(x, y, stone)) > 0:
            return True

        nb_free_three = self._is_free_three_dir(x, y, stone, 1, 0) + \
                        self._is_free_three_dir(x, y, stone, 0, 1) + \
                        self._is_free_three_dir(x, y, stone, 1, 1) + \
                        self._is_free_three_dir(x, y, stone, -1, 1)
        if nb_free_three >= 2:
            return False  # double three
        return True

    def print_board(self):
        """
        print the board (with colors) on stdout
        """
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
                if self.content[y][x]['stone'] == STONE_EMPTY:
                    pass
                elif self.content[y][x]['stone'] == 0:
                   color = [c.WHITE, c.F_WHITE]
                elif self.content[y][x]['stone'] == 1:
                    color = [c.BLACK, c.F_BLACK]
                elif self.content[y][x]['stone'] == 2:
                    color = [c.RED, c.F_RED]
                elif self.content[y][x]['stone'] == 3:
                    color = [c.GREEN, c.F_GREEN]
                elif self.content[y][x]['stone'] == 4:
                    color = [c.BLUE, c.F_BLUE]
                elif self.content[y][x]['stone'] == 5:
                    color = [c.YELLOW, c.F_YELLOW]
                elif self.content[y][x]['stone'] == 6:
                    color = [c.MAGENTA, c.F_MAGENTA]
                elif self.content[y][x]['stone'] == 7:
                    color = [c.CYAN, c.F_CYAN]
                else:
                    txt = '%2d ' % (self.content[y][x]['stone'])
                print(end=color[0] + color[1] + txt + c.EOC)
            print('|')
        for i in range(self.size):
            if i == 0:
                print(end='*')
            print(end='---')
        if i == self.size - 1:
            print('*')
