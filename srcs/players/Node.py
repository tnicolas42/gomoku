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
        self.board = SoftBoard(self.game, self.game.board.size, parent_content)
        if self.x != -1 and self.y != -1:
            self.board.put_stone(self.x, self.y, self.stone, test=True)

        self.childs = []

    @get_stats
    def get_childs_coord(self):
        testChilds = dict()
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.content[y][x] is not STONE_EMPTY:
                    # add the squares arround the curent pos to testChilds
                    for _y in range(y - G.NB_SQUARE_ARROUND, y + G.NB_SQUARE_ARROUND + 1):
                        for _x in range(x - G.NB_SQUARE_ARROUND, x + G.NB_SQUARE_ARROUND + 1):
                            if _x >= 0 and _x < self.board.size and _y >= 0 and _y < self.board.size:
                                testChilds[(_y, _x)] = True
        return testChilds

    @get_stats
    def setChilds(self):
        testChilds = self.get_childs_coord()

        # self.game.board.reset_debug()
        for y, x in testChilds:
            if self.board.is_allowed(x, y, not self.stone):
                # self.game.board.content_desc[y][x]['debug_marker_color'] = 'red'
                self.childs.append(Node(self.game, self.transpositionTable, not self.stone, x, y, self.depth - 1, self))

