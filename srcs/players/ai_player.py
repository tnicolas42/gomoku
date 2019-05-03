import time
import random
from srcs.players.player import Player
from srcs.players.Node import Node

class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)

    def move(self):
        """
        this function is called when the AI need to move
        -> put a stone on the board
        """
        # first algo -> just put a random stone
        # time.sleep(0.1)
        # while 42:
        #     x = random.randrange(0, self.game.board.size)
        #     y = random.randrange(0, self.game.board.size)
        #     if self.game.board.is_allowed(x, y, self.stone):
        #         self.game.board.put_stone(x, y, self.stone)
        #         return
        # print(self.game.boaboard)

        depth = 2
        nodes = Node(self.game, self.stone, -1, -1, depth)
        print(min_max(nodes, depth, True))

def heuristic(node):
    return random.randint(-1000, 1000)

def is_terminal_node(node):
    return False

def min_max(node, depth, maximize):
    """
    min_max algorithm implementation
    """
    if depth == 0 or is_terminal_node(node):
        return {'_node': node, 'cost': heuristic(node)}
    if maximize:
        _max = float('-inf')
        for child in node.childs:
            childMin = min_max(child, depth-1, True)
            if childMin['cost'] > _max:
                _max = childMin['cost']
                _node = child
        return {'_node': _node, 'cost': _max}
    else:
        _min = float('inf')
        for child in node.childs:
            childMax = min_max(child, depth-1, True)
            if childMax['cost'] < _min:
                _min = childMax['cost']
                _node = child
        return {'_node': _node, 'cost': _min}
