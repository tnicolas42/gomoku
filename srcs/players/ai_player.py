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

    @set_marker()
    @get_and_print_stats()
    def move(self):
        """
        this function is called when the AI need to move
        -> put a stone on the board
        """
        # put the first stone in the middle
        if (self.game.board.remain_places == G.BOARD_SZ * G.BOARD_SZ):
            self.game.board.put_stone(int(G.BOARD_SZ / 2), int(G.BOARD_SZ / 2), self.stone)
        else:
            transpositionTable = {}
            depth = min(G.DEPTH, self.game.board.remain_places)
            nodes = Node(self.game, transpositionTable, not self.stone, -1, -1, depth+1, None)
            # move = min_max(nodes, depth, True, float('-inf'), float('inf'))
            move = iterative_deepening(nodes, depth)
            if move is None:
                return None
            if G.DEBUG_ANTICIPATION:
                for x in range(G.BOARD_SZ):
                    for y in range(G.BOARD_SZ):
                        if self.game.board.content[y][x] == STONE_EMPTY:
                            if move['node'].board.content[y][x] != STONE_EMPTY:
                                self.game.board.content_desc[y][x]['debug_marker_color'] = STONES[move['node'].board.content[y][x]]
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

def iterative_deepening(node, depth):
    firstguess = {'node': None, 'cost': 0}
    for d in range(1, depth + 1):
        # print(depth)
        firstguess = mtdf(node, firstguess, d)
        # print(firstguess)
    return firstguess

def mtdf(node, f, d):
    g = f['cost']
    upperBound = float('inf')
    lowerBound = float('-inf')

    while lowerBound < upperBound:
        beta = max(g, lowerBound + 1)
        # print('-----')
        f = alpha_beta(node, d, False, beta - 1, beta)
        g = f['cost']
        # print(f)
        # print('lowerBound:', lowerBound, 'upperBound:', upperBound)
        # print('g < beta: ', g, '<', beta, '=', g < beta)
        if g < beta:
            upperBound = g
        else:
            lowerBound = g
    return f

def alpha_beta(node, depth, maximize, alpha, beta):
    """
    alpha_beta algorithm implementation
    """
    if node.game.reset_game:
        return None
    if depth == 0 or is_terminal_node(node):
        return {'node': node, 'cost': heuristic(node)}
    if maximize:
        best = float('-inf')
        maxlst = None
        for child in node.childs:
            if best >= beta:
                break
            childMin = alpha_beta(child, depth-1, False, alpha, beta)
            if childMin['cost'] is None:
                continue
            if childMin['cost'] > best:
                best = childMin['cost']
                maxlst = [childMin['node']]
            elif childMin['cost'] == best:
                maxlst.append(childMin['node'])
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        if maxlst is None:
            return {'node': None, 'cost': None}
        if G.MINMAX_RANDOM_CHOICE:
            _node = random.choice(maxlst)
        else:
            _node = maxlst[0]
        return {'node': _node, 'cost': best}
    else:
        best = float('inf')
        minlst = None
        for child in node.childs:
            if best <= alpha:
                break
            childMax = alpha_beta(child, depth-1, True, alpha, beta)
            if childMax['cost'] is None:
                continue
            if childMax['cost'] < best:
                best = childMax['cost']
                minlst = [childMax['node']]
            elif childMax['cost'] == best:
                minlst.append(childMax['node'])
            beta = min(beta, best)
            if beta <= alpha:
                break
        if minlst is None:
            return {'node': None, 'cost': None}
        if G.MINMAX_RANDOM_CHOICE:
            _node = random.choice(minlst)
        else:
            _node = minlst[0]
        return {'node': _node, 'cost': best}
