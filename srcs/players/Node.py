from srcs.board import Board, SoftBoard
from srcs.const import *
from srcs.players.player import Player
from srcs.utils.stats import *


class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + ')'

    @get_stats
    def __init__(self, game, transpositionTable, stone, x, y, depth, parent=None):
        self.game = game
        self.transpositionTable = transpositionTable
        self.parent = parent
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth
        if self.parent:
            parent_content = self.parent.board.content
        else:
            parent_content = self.game.board.content
        self.board = SoftBoard(self.game, parent_content)

        self.childs = []

    @get_stats
    def get_childs_coord(self):
        testChilds = dict()
        for y in range(G.BOARD_SZ):
            for x in range(G.BOARD_SZ):
                if self.board.content[y][x][STONE] is not STONE_EMPTY:
                    # add the squares arround the curent pos to testChilds
                    for _y in range(y - G.NB_SQUARE_ARROUND, y + G.NB_SQUARE_ARROUND + 1):
                        for _x in range(x - G.NB_SQUARE_ARROUND, x + G.NB_SQUARE_ARROUND + 1):
                            if 0 <= _x < G.BOARD_SZ and 0 <= _y < G.BOARD_SZ and self.board.content[_y][_x][STONE] == STONE_EMPTY:
                                testChilds[(_y, _x)] = True
        tmp = self
        while tmp.parent:
            for _y in range(tmp.y - G.NB_SQUARE_ARROUND, tmp.y + G.NB_SQUARE_ARROUND + 1):
                for _x in range(tmp.x - G.NB_SQUARE_ARROUND, tmp.x + G.NB_SQUARE_ARROUND + 1):
                    if 0 <= _x < G.BOARD_SZ and 0 <= _y < G.BOARD_SZ and self.board.content[_y][_x][STONE] == STONE_EMPTY:
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
            self.childs.append(Node(self.game, self.transpositionTable, not self.stone, x, y, self.depth - 1, self))

