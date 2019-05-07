import time
import random
from srcs.heuristic import get_heuristic
from srcs.players.player import Player
from srcs.players.Node import Node
from srcs.utils.stats import *
from srcs.const import *

class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        Player.__init__(self, *args, **kwargs)

    @get_and_print_stats()
    def move(self):
        """
        this function is called when the AI need to move
        -> put a stone on the board
        """
        # put the first stone in the middle
        if (self.game.board.remain_places == self.game.board.size * self.game.board.size):
            self.game.board.put_stone(int(self.game.board.size / 2), int(self.game.board.size / 2), self.stone)
        else:
            transpositionTable = {}
            nodes = Node(self.game, transpositionTable, not self.stone, -1, -1, DEPTH+1, None)
            move = min_max(nodes, DEPTH, True, float('-inf'), float('inf'))
            # print('heurisitic: %f' % (get_heuristic(move['node'], printDebug=True)))
            # for x in range(self.game.board.size):
            #     for y in range(self.game.board.size):
            #         if self.game.board.content[y][x] == STONE_EMPTY:
            #             if move['node'].board.content[y][x] != STONE_EMPTY:
            #                 self.game.board.content_desc[y][x]['debug_marker_color'] = STONES[move['node'].board.content[y][x]]
            node = move['node']
            while node.parent.parent:
                node = node.parent
            self.game.board.put_stone(node.x, node.y, self.stone)

def heuristic(node):
    res = get_heuristic(node)
    return res

def is_terminal_node(node):
    node.setChilds()
    return len(node.childs) == 0

def min_max(node, depth, maximize, alpha, beta):
    """
    min_max algorithm implementation
    """
    if depth == 0 or is_terminal_node(node):
        return {'node': node, 'cost': heuristic(node)}
    if maximize:
        _max = float('-inf')
        maxlst = []
        for child in node.childs:
            childMin = min_max(child, depth-1, False, alpha, beta)
            if childMin['cost'] > _max:
                _max = childMin['cost']
                maxlst = [childMin['node']]
                # maxlst = [child]
            elif childMin['cost'] == _max:
                maxlst.append(childMin['node'])
                # maxlst.append(child)
            alpha = max(alpha, _max)
            if beta <= alpha:
                break
        # _node = random.choice(maxlst)
        _node = maxlst[0]
        return {'node': _node, 'cost': _max}
    else:
        _min = float('inf')
        minlst = []
        for child in node.childs:
            childMax = min_max(child, depth-1, True, alpha, beta)
            if childMax['cost'] < _min:
                _min = childMax['cost']
                minlst = [childMax['node']]
                # minlst = [child]
            elif childMax['cost'] == _min:
                minlst.append(childMax['node'])
                # minlst.append(child)
            beta = min(beta, _min)
            if beta <= alpha:
                break
        # _node = random.choice(minlst)
        _node = minlst[0]
        return {'node': _node, 'cost': _min}
