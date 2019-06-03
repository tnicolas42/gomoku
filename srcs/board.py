from srcs.const import *
from srcs.utils.stats import get_stats, get_and_print_stats

class SoftBoard(object):
    """
    this is the game board
    it contains a matrix (content) that contains info about the board:
    [
        [{}, {}, {}, ...]
        [{}, {}, {}, ...]
        ...
    ]
    foreach dictionnary:
        stone=int
            -1 == empty place
            0, 1, ... == stone
        vulnerability=bool
            if vulneable (can be destroyed with one move) -> True else False
        win=bool
        debug_color=str
            if not None -> set the outline of the stone with the color: 'debug_color'
        debug_marker_color=str
            if not None -> put a marker on this position
    """
    game = None  # the game object
    softMode = True
    content = []  # this is the board
    content_desc = None  # content description -> vulnerability, win, ...
    remain_places = None  # number of remaining places
    is_vulnerable_victory = None  # if victory but vulnerable -> wait one turn before win
    nb_total_stones = 0  # total number of stone on board

    def __init__(self, game, content=[]):
        self.game = game
        self.content = [
            [
                STONE_EMPTY if content == [] else content[j][i]  # player id or STONE_EMPTY
            for i in range(G.GET("BOARD_SZ"))] for j in range(G.GET("BOARD_SZ"))
        ]
        # True if vulnerable (BAA.)
        self.vulnerability = [
            [False for i in range(G.GET("BOARD_SZ"))] for j in range(G.GET("BOARD_SZ"))
        ]
        self.remain_places = G.GET("BOARD_SZ") * G.GET("BOARD_SZ")

    def check_vulnerability(self, x, y):
        """
        check the vulnerability of one stone
        """
        stone = self.content[y][x]
        if stone == STONE_EMPTY:
            return False
        # for 4 stones: abcd with b is x y -> a=x1y1 b=xy c=x2y2 d=x3y3
        vul_cond = lambda x1, y1, x2, y2, x3, y3: (
                        0 <= x1 < G.GET("BOARD_SZ") and 0 <= x2 < G.GET("BOARD_SZ") and 0 <= x3 < G.GET("BOARD_SZ") and
                        0 <= y1 < G.GET("BOARD_SZ") and 0 <= y2 < G.GET("BOARD_SZ") and 0 <= y3 < G.GET("BOARD_SZ") and
                        stone == self.content[y2][x2] and
                        self.content[y1][x1] != stone and self.content[y3][x3] != stone and
                        self.content[y1][x1] != self.content[y3][x3] and
                        (self.content[y1][x1] == STONE_EMPTY or self.content[y3][x3] == STONE_EMPTY))
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
                self.vulnerability[y][x] = True
                return True
        self.vulnerability[y][x] = False
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
                        0 <= x1 < G.GET("BOARD_SZ") and 0 <= x2 < G.GET("BOARD_SZ") and 0 <= x3 < G.GET("BOARD_SZ") and
                        0 <= y1 < G.GET("BOARD_SZ") and 0 <= y2 < G.GET("BOARD_SZ") and 0 <= y3 < G.GET("BOARD_SZ") and
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
                ret.append([destroy_tab_i[0], destroy_tab_i[1]])
                ret.append([destroy_tab_i[2], destroy_tab_i[3]])

        return ret

    def _check_aligned_dir(self, x, y, stone, addx, addy, check_only=False):
        """
        check the alignement in one direction (given by addx and addy)

        if check_only -> don't update the player victory

        return bool (if 5 or more aligned) and bool (if he aligneement is not vulnerable)
        """
        nb_aligned = 1
        is_aligned_vulnerable = [False, False]
        if self.vulnerability[y][x]:
            is_aligned_vulnerable = [True, True]
        nb_aligned_non_vulnerable = 1
        new_x = x + addx
        new_y = y + addy
        while 0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ"):
            if self.content[new_y][new_x] == stone:
                if self.vulnerability[new_y][new_x]:
                    is_aligned_vulnerable[0] = True
                if not is_aligned_vulnerable[0]:
                    nb_aligned_non_vulnerable += 1
                nb_aligned += 1
            else:
                break
            new_x += addx
            new_y += addy
        new_x = x - addx
        new_y = y - addy
        while 0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ"):
            if self.content[new_y][new_x] == stone:
                if self.vulnerability[new_y][new_x]:
                    is_aligned_vulnerable[1] = True
                if not is_aligned_vulnerable[1]:
                    nb_aligned_non_vulnerable += 1
                nb_aligned += 1
            else:
                break
            new_x -= addx
            new_y -= addy
        if nb_aligned >= G.GET("NB_ALIGNED_VICTORY"):
            if not check_only:
                new_x = x
                new_y = y
                while 0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ"):
                    if self.content[new_y][new_x] == stone:
                        if not self.softMode and \
                           (self.is_vulnerable_victory[stone] or nb_aligned_non_vulnerable >= G.GET("NB_ALIGNED_VICTORY")):
                            self.content_desc[new_y][new_x]['win'] = True
                    else:
                        break
                    new_x += addx
                    new_y += addy
                new_x = x - addx
                new_y = y - addy
                while 0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ"):
                    if self.content[new_y][new_x] == stone:
                        if not self.softMode and \
                           (self.is_vulnerable_victory[stone] or nb_aligned_non_vulnerable >= G.GET("NB_ALIGNED_VICTORY")):
                            self.content_desc[new_y][new_x]['win'] = True
                    else:
                        break
                    new_x -= addx
                    new_y -= addy
            if nb_aligned_non_vulnerable >= G.GET("NB_ALIGNED_VICTORY"):
                return True, True  # nb_aligned == OK, not_vulnerable == True
            else:
                return True, False  # nb_aligned == OK, not_vulerable == False -> wait one turn before win
        return False, False  # nb_aligned too low

    def check_aligned(self, x, y, check_only=False):
        """
        check if there is 5 or more aligned stones
        also check vulnerability of all stones

        if check_only -> don't update player victory

        return the new state of is_vulnerable_victory
        """
        stone = self.content[y][x]
        if stone == STONE_EMPTY:
            return False
        total_is_aligned = False
        total_is_not_vulnerable = False

        is_aligned, is_not_vulnerable = self._check_aligned_dir(x, y, stone, 1, 0, check_only)
        total_is_aligned = total_is_aligned or is_aligned
        total_is_not_vulnerable = total_is_not_vulnerable or is_not_vulnerable
        is_aligned, is_not_vulnerable = self._check_aligned_dir(x, y, stone, 0, 1, check_only)
        total_is_aligned = total_is_aligned or is_aligned
        total_is_not_vulnerable = total_is_not_vulnerable or is_not_vulnerable
        is_aligned, is_not_vulnerable = self._check_aligned_dir(x, y, stone, 1, 1, check_only)
        total_is_aligned = total_is_aligned or is_aligned
        total_is_not_vulnerable = total_is_not_vulnerable or is_not_vulnerable
        is_aligned, is_not_vulnerable = self._check_aligned_dir(x, y, stone, 1, -1, check_only)
        total_is_aligned = total_is_aligned or is_aligned
        total_is_not_vulnerable = total_is_not_vulnerable or is_not_vulnerable

        if total_is_aligned:
            if not check_only:
                if self.is_vulnerable_victory[stone] or total_is_not_vulnerable:
                    self.game.players[stone].is_win_aligned = True
                if not total_is_not_vulnerable:  # if vulnerable
                    return True
            else:
                return True
        return False

    def check_winner(self):
        if self.is_vulnerable_victory == None:
            self.is_vulnerable_victory = [False for i in range(len(self.game.players))]

        self.nb_total_stones = 0
        for pl in self.game.players:
            pl.nb_stone = 0
        for x in range(G.GET("BOARD_SZ")):
            for y in range(G.GET("BOARD_SZ")):
                if self.content[y][x] is not STONE_EMPTY:
                    self.nb_total_stones += 1
                    self.game.players[self.content[y][x]].nb_stone += 1
                self.check_vulnerability(x, y)

        tmp_is_vulnerable_victory = [False for i in range(len(self.game.players))]
        for x in range(G.GET("BOARD_SZ")):
            for y in range(G.GET("BOARD_SZ")):
                tmp_is_vulnerable_victory[self.content[y][x]] = tmp_is_vulnerable_victory[self.content[y][x]] or self.check_aligned(x, y)
        self.is_vulnerable_victory = tmp_is_vulnerable_victory

    def put_stone(self, x, y, stone, test=False):
        """
        put a stone at 'x' 'y' with id 'stone'
        this function put a stone and, if needed, destroy some stones:
        before  -> -1  0  0  1
        put     ->  1  0  0  1
        destroy ->  1 -1 -1  1

        this function can also count the number of stones aligned with the putted stone to know if the player win
        if the player win -> update player.is_win_aligned
        """
        if x >= G.GET("BOARD_SZ") or y >= G.GET("BOARD_SZ"):
            print("[ERROR]: unable to put a stone at %d %d -> out of board" % (x, y))
            exit(1)

        if not test:
            self.game.gui.gui_game.last_pos = [x, y]  # save the pos of the last placed stone
            self.remain_places -= 1
        self.content[y][x] = stone

        # destroy some stones if needed
        destroyed = self.check_destroyable(x, y, stone)
        for dest_x, dest_y in destroyed:
            self.content[dest_y][dest_x] = STONE_EMPTY
            self.remain_places += 1
            if not test:
                self.game.players[stone].destroyed_stones_count += 1

        if not test:
            # check aif there is a winner
            self.check_winner()

        return destroyed

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
        lst = [-2 for i in range(len(free_three[0]))]
        i = 0
        new_x = x - (addx * (len_free_three >> 1))
        new_y = y - (addy * (len_free_three >> 1))
        while i < len_free_three:
            if 0 <= new_x < G.GET("BOARD_SZ") and 0 <= new_y < G.GET("BOARD_SZ"):
                lst[i] = self.content[new_y][new_x]
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
        if self.content[y][x] is not STONE_EMPTY:
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
            self.content[y][x] = stone
            check_aligned = self.check_aligned(x, y, True)  # if the move win
            self.content[y][x] = STONE_EMPTY
            if check_aligned:
                return True
            else:
                return False  # double three
        return True

    def __str__(self):
        """
        print the board (with colors) on stdout
        """
        s = ''
        for i in range(G.GET("BOARD_SZ")):
            if i == 0:
                s += '*'
            s += '---'
        if i == G.GET("BOARD_SZ") - 1:
            s += '*\n'
        for y in range(G.GET("BOARD_SZ")):
            s += '|'
            for x in range(G.GET("BOARD_SZ")):
                color = [c.EOC, c.EOC]
                txt = ' . '
                if self.content[y][x] == STONE_EMPTY:
                    pass
                elif self.content[y][x] == 0:
                    color = [c.CYAN, c.F_CYAN]
                elif self.content[y][x] == 1:
                    color = [c.WHITE, c.F_WHITE]
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
                    color = [c.BLACK, c.F_BLACK]
                else:
                    txt = '%2d ' % (self.content[y][x])
                s += color[0] + color[1] + txt + c.EOC
            s += '|\n'
        for i in range(G.GET("BOARD_SZ")):
            if i == 0:
                s += '*'
            s += '---'
        if i == G.GET("BOARD_SZ") - 1:
            s += '*'
        return s

class Board(SoftBoard):
    """
    this is the game board
    it contains a matrix (content) that contains info about the board:
    [
        [{}, {}, {}, ...]
        [{}, {}, {}, ...]
        ...
    ]
    foreach dictionnary:
        stone=int
            -1 == empty place
            0, 1, ... == stone
        vulnerability=bool
            if vulneable (can be destroyed with one move) -> True else False
        win=bool
        debug_color=str
            if not None -> set the outline of the stone with the color: 'debug_color'
        debug_marker_color=str
            if not None -> put a marker on this position
    """
    softMode = False

    def __init__(self, *args, **kwargs):
        SoftBoard.__init__(self, *args, **kwargs)
        self.content_desc = [
            [
                {
                    'win': 0,  # True if the player win wit this stone
                    'debug_color': None,  # set an outline of this color around stones
                    'debug_marker_color': None,  # set a marker of this color one this point (even on EMPTY STONES)
                    'debug_txt': None,  # show text (tuple: [text, color])
                }
            for i in range(G.GET("BOARD_SZ"))] for j in range(G.GET("BOARD_SZ"))
        ]

    def reset_debug(self):
        """
        reset the debug color in all the board
        """
        for x in range(G.GET("BOARD_SZ")):
            for y in range(G.GET("BOARD_SZ")):
                self.content_desc[y][x]['debug_color'] = None
                self.content_desc[y][x]['debug_marker_color'] = None
                self.content_desc[y][x]['debug_txt'] = None
