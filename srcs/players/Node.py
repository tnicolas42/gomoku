from srcs.board import Board, SoftBoard
from srcs.const import *
from srcs.players.player import Player
from srcs.utils.stats import *


class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + '->' + str(self.heuristic) + ')'

    def __init__(self, game, transpositionTable, stone, depth, x=-1, y=-1, parent=None):
        self.game = game
        self.transpositionTable = transpositionTable
        self.parent = parent
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth
        if self.parent:
            self.board = self.parent.board
            self.childs_test_coord = self.parent.childs_test_coord
        else:
            self.board = SoftBoard(self.game, self.game.board.content)
            self.childs_test_coord = dict()
        self.changes = [[self.x, self.y, STONE_EMPTY]]

        self.childs = []
        self.heuristic = None
        self.is_win = False

    def reset_board(self):
        node = self
        while node.parent:
            for x, y, stone in node.changes:
                node.board.content[y][x] = stone
            node = node.parent

    def init_child_coord(self):
        self.child_coord = dict()
        for y in range(G.GET("BOARD_SZ")):
            for x in range(G.GET("BOARD_SZ")):
                if self.board.content[y][x] is not STONE_EMPTY:
                    # add the squares arround the curent pos to testChilds
                    for _y in range(y - G.GET("NB_SQUARE_ARROUND"), y + G.GET("NB_SQUARE_ARROUND") + 1):
                        for _x in range(x - G.GET("NB_SQUARE_ARROUND"), x + G.GET("NB_SQUARE_ARROUND") + 1):
                            if 0 <= _x < G.GET("BOARD_SZ") and 0 <= _y < G.GET("BOARD_SZ") and self.board.content[_y][_x] == STONE_EMPTY:
                                self.child_coord[(_y, _x)] = True

    def get_childs_coord(self):
        testChilds = dict()
        dontTest = dict()
        tmp = self
        while tmp.parent:
            dontTest[(tmp.y, tmp.x)] = True
            tmp = tmp.parent
        return testChilds, dontTest

    @get_stats
    def setChilds(self):
        self.init_child_coord()
        testChilds, dontTest = self.get_childs_coord()

        for y, x in self.child_coord:
            if (y, x) in dontTest:
                continue
            if G.DEBUG_SEARCH_ZONE:
                self.game.board.content_desc[y][x]['debug_marker_color'] = 'red'
            self.childs.append(Node(self.game, self.transpositionTable, not self.stone, x, y, self.depth - 1, self))

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