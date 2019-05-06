import time
import random
from srcs.heuristic import basic_heuristic
from srcs.utils.stats import *
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
        depth = 2
        nodes = Node(self.game, not self.stone, -1, -1, depth+1, None)
        move = min_max(nodes, depth, True)
        self.game.board.put_stone(move['node'].x, move['node'].y, self.stone)

def heuristic(node):
    res = basic_heuristic(node)
    return res

def is_terminal_node(node):
    return len(node.childs) == 0

@get_stats
def min_max(node, depth, maximize):
    """
    min_max algorithm implementation
    """
    if depth == 0 or is_terminal_node(node):
        return {'node': node, 'cost': heuristic(node)}
    if maximize:
        _max = float('-inf')
        maxlst = []
        for child in node.childs:
            childMin = min_max(child, depth-1, False)
            if childMin['cost'] > _max:
                _max = childMin['cost']
                maxlst = [child]
            elif childMin['cost'] == _max:
                maxlst.append(child)
            _node = random.choice(maxlst)
        return {'node': _node, 'cost': _max}
    else:
        _min = float('inf')
        minlst = []
        for child in node.childs:
            childMax = min_max(child, depth-1, True)
            if childMax['cost'] < _min:
                _min = childMax['cost']
                minlst = [child]
            elif childMax['cost'] == _min:
                minlst.append(child)
            _node = random.choice(minlst)
        return {'node': _node, 'cost': _min}
