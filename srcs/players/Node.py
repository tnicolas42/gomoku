from srcs.players.player import Player
from srcs.utils.stats import get_stats, get_and_print_stats
from srcs.board import Board

class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + ')'

    @get_stats
    def __init__(self, game, stone, x, y, depth, parent=None):
        self.game = game
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth
        self.board = Board(self.game, self.game.board.size, self.game.board.content.copy())
        if self.x != -1 and self.y != -1:
            self.board.put_stone(self.x, self.y, self.stone, test=True)

        self.parent = parent
        self.childs = []
        if depth > 0:
            self.setChilds()

    def setChilds(self):
        for y in range(self.game.board.size):
            for x in range(self.game.board.size):
                if self.game.board.is_allowed(x, y, self.stone):
                    if not self.parent or (self.parent and not (self.parent.x == x and self.parent.y == y)):
                        self.childs.append(Node(self.game, self.stone, x, y, self.depth - 1, self))
