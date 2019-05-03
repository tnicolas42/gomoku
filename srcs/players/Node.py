from srcs.players.player import Player
from srcs.utils.stats import get_stats, get_and_print_stats

class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + ')'

    @get_stats
    def __init__(self, game, stone, x, y, depth):
        self.game = game
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth

        self.childs = []
        if depth > 0:
            self.setChilds()

    def setChilds(self):
        for y in range(self.game.board.size):
            for x in range(self.game.board.size):
                if self.game.board.is_allowed(x, y, self.stone):
                    self.childs.append(Node(self.game, self.stone, x, y, self.depth - 1))