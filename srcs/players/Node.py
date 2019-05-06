from srcs.players.player import Player
from srcs.board import Board

class Node():
    """
    this function store a possible move for the ai minMax algorithm
    """
    def __repr__(self):
        return '(' + str(self.x) + ':' + str(self.y) + ')'

    def __init__(self, game, stone, x, y, depth, parent=None):
        self.game = game
        self.parent = parent
        self.stone = stone
        self.x = x
        self.y = y
        self.depth = depth
        if self.parent:
            parent_content = self.parent.board.content
        else:
            parent_content = self.game.board.content
        self.board = Board(self.game, self.game.board.size, parent_content)
        if self.x != -1 and self.y != -1:
            self.board.put_stone(self.x, self.y, self.stone, test=True)

        self.childs = []
        if depth > 0:
            self.setChilds()

    def setChilds(self):
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.is_allowed(x, y, not self.stone):
                    if not self.parent or (self.parent and not (self.parent.x == x and self.parent.y == y)):
                        self.childs.append(Node(self.game, not self.stone, x, y, self.depth - 1, self))
