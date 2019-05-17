from srcs.board import Board, SoftBoard
from srcs.const import *
from srcs.players.player import Player
from srcs.utils.stats import *
from srcs.utils.u_board import _at, _set


class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + '->' + str(self.heuristic) + ')'

    def __init__(self, game, transpositionTable, stone, x, y, depth, parent=None):
        self.game = game
        self.transpositionTable = transpositionTable
        self.parent = parent
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth
        parent_content = self.parent.board.content if self.parent else self.game.board.content
        self.board = SoftBoard(self.game, parent_content)

        self.childs = []
        self.heuristic = None
        self.is_win = False

    def get_childs_coord(self):
        testChilds = dict()
        for y in range(G.GET("BOARD_SZ")):
            for x in range(G.GET("BOARD_SZ")):
                if _at(self.board.content, x, y) != STONE_EMPTY:
                    # add the squares arround the curent pos to testChilds
                    for _y in range(y - G.GET("NB_SQUARE_ARROUND"), y + G.GET("NB_SQUARE_ARROUND") + 1):
                        for _x in range(x - G.GET("NB_SQUARE_ARROUND"), x + G.GET("NB_SQUARE_ARROUND") + 1):
                            if 0 <= _x < G.GET("BOARD_SZ") and 0 <= _y < G.GET("BOARD_SZ") and _at(self.board.content, _x, _y) == STONE_EMPTY:
                                testChilds[(_y, _x)] = True
        tmp = self
        while tmp.parent:
            for _y in range(tmp.y - G.GET("NB_SQUARE_ARROUND"), tmp.y + G.GET("NB_SQUARE_ARROUND") + 1):
                for _x in range(tmp.x - G.GET("NB_SQUARE_ARROUND"), tmp.x + G.GET("NB_SQUARE_ARROUND") + 1):
                    if 0 <= _x < G.GET("BOARD_SZ") and 0 <= _y < G.GET("BOARD_SZ") and _at(self.board.content, _x, _y) == STONE_EMPTY:
                        testChilds[(_y, _x)] = True
            tmp = tmp.parent
        return testChilds

    @get_stats
    def setChilds(self):
        testChilds = self.get_childs_coord()

        if G.DEBUG_SEARCH_ZONE:
            self.game.board.reset_debug()
        for y, x in testChilds:
            if G.DEBUG_SEARCH_ZONE:
                self.game.board.content_desc[y][x]['debug_marker_color'] = 'red'
            self.childs.append(Node(self.game, self.transpositionTable, (not (self.stone - 1)) + 1, x, y, self.depth, self))

    # compare function <
    def __lt__(self, other):
        if self.heuristic == None:
            return False
        elif other.heuristic == None:
            return True
        return self.heuristic < other.heuristic

    # compare function <=
    def __le__(self, other):
        if self.heuristic == None:
            return False
        elif other.heuristic == None:
            return True
        return self.heuristic <= other.heuristic

    # compare function >=
    def __ge__(self, other):
        if self.heuristic == None:
            return False
        elif other.heuristic == None:
            return True
        return self.heuristic >= other.heuristic

    # compare function >
    def __gt__(self, other):
        if self.heuristic == None:
            return False
        elif other.heuristic == None:
            return True
        return self.heuristic > other.heuristic